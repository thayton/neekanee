import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify

from neekanee_solr.models import *

COMPANY = {
    'name': 'Systech',
    'hq': 'San Diego, CA',

    'home_page_url': 'http://www.systech.com',
    'jobs_page_url': 'http://www.systech.com/resources-mainmenu-87/employment-opportunities-mainmenu-109.html',

    'empcnt': [11,50]
}

class SysTechJobScraper(JobScraper):
    def __init__(self):
        super(SysTechJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)
        s = soupify(self.br.response().read())

        self.company.job_set.all().delete()

        for h in s.findAll('h3'):
            job = Job(company=self.company)
            job.title = h.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = ''

            x = h.nextSibling

            while getattr(x, 'name', None) != 'hr':
                if hasattr(x, 'name') is False: 
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return SysTechJobScraper()
