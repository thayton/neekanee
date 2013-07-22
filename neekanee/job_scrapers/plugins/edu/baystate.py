import re, urllib, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Bay State College',
    'hq': 'Boston, MA',

    'home_page_url': 'http://www.baystate.edu',
    'jobs_page_url': 'http://www.baystate.edu/about-baystate/employment/current-opportunities/',

    'empcnt': [51,200]
}

class BayStateJobScraper(JobScraper):
    def __init__(self):
        super(BayStateJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'/employment/current-opportunities/details/\d+/')

        for a in s.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.location = self.company.location
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            x = soupify(self.br.response().read())
            d = x.find('div', id='page')

            job.desc =  get_all_text(d)
            job.save()

def get_scraper():
    return BayStateJobScraper()
