import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Whitney Museum Of American Art',
    'hq': 'New York, NY',

    'contact': 'hr@whitney.org',
    'benefits': {'vacation': []},

    'home_page_url': 'http://whitney.org',
    'jobs_page_url': 'http://whitney.org/About/JobPostings',

    'empcnt': [51,200]
}

class WhitneyJobScraper(JobScraper):
    def __init__(self):
        super(WhitneyJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='layout-modules')
        x = {'class': 'expand-collapse-module-content-column'}

        self.company.job_set.all().delete()

        for td in d.findAll('td', attrs=x):
            v = td.findAll('div')[-1]

            job = Job(company=self.company)
            job.title = td.h2.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = get_all_text(v)
            job.save()

def get_scraper():
    return WhitneyJobScraper()
