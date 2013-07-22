import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Kimpton Hotels & Restaurants',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.kimptonhotels.com',
    'jobs_page_url': 'http://www.kimptonhotels.com/careers/jobsearch.aspx',

    'empcnt': [5001,10000]
}

class KimptonHotelsJobScraper(JobScraper):
    def __init__(self):
        super(KimptonHotelsJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)
        self.br.follow_link(self.br.find_link(tag='iframe'))

        def select_form(form):
            return form.method == 'GET' and form.attrs.has_key('action') and \
                form.attrs['action'].endswith('search-results')

        self.br.select_form(predicate=select_form)
        self.br.submit(name='form.commit')

        s = soupify(self.br.response().read())
        r = re.compile(r'view\?jobAdId=\d+$')

        for a in s.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = self.parse_location(td[1].text)
            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = l
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())

            job.desc = get_all_text(s.html)
            job.save()

def get_scraper():
    return KimptonHotelsJobScraper()
