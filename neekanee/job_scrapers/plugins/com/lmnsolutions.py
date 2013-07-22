import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'LMN Solutions',
    'hq': 'Reston, VA',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.lmnsolutions.com',
    'jobs_page_url': 'http://jobs.lmnsolutions.com',

    'empcnt': [11,50]
}

class LmnSolutionsJobScraper(JobScraper):
    def __init__(self):
        super(LmnSolutionsJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        v = s.find('div', id='test')

        for d in v.findAll('div', id='job'):
            l = d.findAll('div')[-1].text
            l = self.parse_location(l)

            if l is None:
                continue

            job = Job(company=self.company)
            job.title = d.h3.a.text
            job.url  = urlparse.urljoin(self.br.geturl(), d.h3.a['href'])
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
            d = s.find('div', id='maincontent-wrap')
            d = d.find('div', style=True)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return LmnSolutionsJobScraper()
