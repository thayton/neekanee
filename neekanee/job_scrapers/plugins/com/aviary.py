import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Aviary',
    'hq': 'New York, NY',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.aviary.com',
    'jobs_page_url': 'http://www.aviary.com/jobs',

    'empcnt': [11,50]
}

class AviaryJobScraper(JobScraper):
    def __init__(self):
        super(AviaryJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        x = {'class': 'job_listing'}

        self.company.job_set.all().delete()

        for d in s.findAll('div', attrs=x):
            l = d.find('div', attrs={'class': 'job_left'})
            r = d.find('div', attrs={'class': 'job_right'})

            job = Job(company=self.company)
            job.title = l.h3.text
            job.url = self.br.geturl()
            job.desc = get_all_text(r)
            job.location = self.company.location
            job.save()

def get_scraper():
    return AviaryJobScraper()

