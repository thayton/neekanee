import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Evernote',
    'hq': 'Mountain View, CA',

    'home_page_url': 'http://www.evernote.com',
    'jobs_page_url': 'http://www.evernote.com/about/careers/',

    'empcnt': [11,50]
}

class EvernoteJobScraper(JobScraper):
    def __init__(self):
        super(EvernoteJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='jobFeed')
        r = re.compile(r'theresumator\.com/apply/\S+/\S+\.html$')
        x = {'href': r, 'target': '_blank'}

        for a in d.findAll('a', attrs=x):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            p = s.find('span', id='resumator-job-location')
            d = s.find('div', id='main')
            l = self.parse_location(p.text)

            if not l:
                continue

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return EvernoteJobScraper()
