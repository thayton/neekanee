import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Quirky',
    'hq': 'New York, NY',

    'home_page_url': 'http://www.quirky.com',
    'jobs_page_url': 'http://www.quirky.com/about/careers',

    'empcnt': [1,10]
}

class QuirkyJobScraper(JobScraper):
    def __init__(self):
        super(QuirkyJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        x = {'class': 'jobs'}
        dl = s.find('dl', attrs=x)
        dl.extract()

        self.company.job_set.all().delete()

        for dt in dl.findAll('dt'):
            dd = dt.findNext('dd')

            job = Job(company=self.company)
            job.title = dt.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = get_all_text(dd)
            job.save()

def get_scraper():
    return QuirkyJobScraper()
