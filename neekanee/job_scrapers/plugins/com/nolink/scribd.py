import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Scribd',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.scribd.com',
    'jobs_page_url': 'http://www.scribd.com/jobs',

    'empcnt': [11,50]
}

class ScribdJobScraper(JobScraper):
    def __init__(self):
        super(ScribdJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        jobs = []

        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        x = {'class': 'job_title'}

        self.company.job_set.all().delete()

        for d in s.findAll('div', attrs=x):
            job = Job(company=self.company)
            job.title = d.h3.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return ScribdJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
