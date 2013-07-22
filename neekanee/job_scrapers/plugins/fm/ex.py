import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'ExFM',
    'hq': 'New York, NY',

    'home_page_url': 'http://ex.fm',
    'jobs_page_url': 'http://ex.fm/jobs',

    'empcnt': [1,10]
}

class ExJobScraper(JobScraper):
    def __init__(self):
        super(ExJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        v = s.find('div', id='job_openings')
        a = { 'class': 'job_opening' }

        self.company.job_set.all().delete()

        for d in v.findAll('div', attrs=a):
            job = Job(company=self.company)
            job.title = d.div.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return ExJobScraper()
