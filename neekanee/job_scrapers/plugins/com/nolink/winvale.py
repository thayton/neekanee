import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Winvale',
    'hq': 'Washington, DC',

    'home_page_url': 'http://www.winvale.com',
    'jobs_page_url': 'http://www.winvale.com/company/careers/',

    'empcnt': [11,50]
}

class WinValeJobScraper(JobScraper):
    def __init__(self):
        super(WinValeJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='careers_sections')

        self.company.job_set.all().delete()

        for x in d.findAll('div', recursive=False):
            job = Job(company=self.company)
            job.title = x.h2.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = get_all_text(x.div) 
            job.save()

def get_scraper():
    return WinValeJobScraper()
