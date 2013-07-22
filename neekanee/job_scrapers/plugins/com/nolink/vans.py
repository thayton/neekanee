import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Vans',
    'hq': 'Cypress, CA',

    'home_page_url': 'http://www.vans.com',
    'jobs_page_url': 'http://www.vans.com/careers/corporate/us',

    'empcnt': [1001,5000]
}

class VansJobScraper(JobScraper):
    def __init__(self):
        super(VansJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        x = {'class': 'job-header'}
        y = {'class': 'job-description'}

        self.company.job_set.all().delete()

        for a in s.findAll('a', attrs=x):
            d = a.findNext('div', attrs=y)
            job = Job(company=self.company)
            job.title = a.text
            job.url = d.a['href'].strip()
            job.location = self.company.location
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return VansJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
