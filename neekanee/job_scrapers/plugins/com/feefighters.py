import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'FeeFighters',
    'hq': 'Chicago, IL',

    'benefits': {'vacation': []},

    'home_page_url': 'http://feefighters.com',
    'jobs_page_url': 'http://feefighters.com/jobs',

    'empcnt': [1,10]
}

class FeeFightersJobScraper(JobScraper):
    def __init__(self):
        super(FeeFightersJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        f = lambda tag: tag.name == 'a' and tag.h3

        for a in s.findAll(f):
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
            d = s.h1.findParent('div')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return FeeFightersJobScraper()

