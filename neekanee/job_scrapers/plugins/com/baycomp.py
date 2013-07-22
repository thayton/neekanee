import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify

from neekanee_solr.models import *

COMPANY = {
    'name': 'Bay Computer Associates',
    'hq': 'Cranston, RI',

    'contact': 'employment@baycomp.com',
    'benefits': {'vacation': []},

    'home_page_url': 'http://www.baycomp.com',
    'jobs_page_url': 'https://www.baycomp.com/CurrentOpenings.aspx',

    'empcnt': [11,50]
}

class BayCompJobScraper(JobScraper):
    def __init__(self):
        super(BayCompJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        a = {'class': 'top-right-corner'}
        d = s.find('div', attrs=a)
        d.extract()

        self.company.job_set.all().delete()

        for h in d.findAll('h3'):
            job = Job(company=self.company)
            job.title = h.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = ''

            x = h.next
            while x and getattr(x, 'name', None) != 'h3':
                if hasattr(x, 'name') is False: 
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return BayCompJobScraper()
