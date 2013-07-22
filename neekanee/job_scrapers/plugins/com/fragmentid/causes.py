import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Causes',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.causes.com',
    'jobs_page_url': 'http://www.causes.com/jobs',

    'empcnt': [11,50]
}

class CausesJobScraper(JobScraper):
    def __init__(self):
        super(CausesJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', attrs={'class': 'jobs'})
        d.extract()

        self.company.job_set.all().delete()

        for h4 in d.findAll('h4'):
            job = Job(company=self.company)
            job.title = h4.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = ''

            x = h4.next

            while x and getattr(x, 'name', None) != 'h4':
                if hasattr(x, 'name') is False: 
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return CausesJobScraper()


