import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'World Health Organization',
    'hq': 'Geneva, Switzerland',

    'home_page_url': 'http://www.who.int',
    'jobs_page_url': 'http://www.who.int/employment/vacancies/en/',

    'empcnt': [5001,10000]
}

class WhoJobScraper(JobScraper):
    def __init__(self):
        super(WhoJobScraper, self).__init__(COMPANY, return_usa_only=False)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='content')
        x = {'class': 'vacancy_headline'}

        for p in d.findAll('span', attrs=x):
            job = Job(company=self.company)
            job.title = p.text
            job.url = urlparse.urljoin(self.br.geturl(), p.a['href'])
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            r = re.compile(r'Duty Station:', re.I)
            l = s.find(text=r)
            t = l.findParent('table')
            l = self.parse_location(l.parent.nextSibling)

            if not l:
                continue

            job.location = l
            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return WhoJobScraper()
