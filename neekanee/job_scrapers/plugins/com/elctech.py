import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'ELC',
    'hq': 'San Francisco, CA',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.elctech.com',
    'jobs_page_url': 'http://elctech.com/careers',

    'empcnt': [11,50]
}

class ElcJobScraper(JobScraper):
    def __init__(self):
        super(ElcJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        v = s.find('div', attrs={'class': 'container'})
        a = {'class': 'jobpost'}

        self.company.job_set.all().delete()

        for d in v.findAll('div', attrs=a):
            job = Job(company=self.company)
            job.title = d.h5.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return ElcJobScraper()
