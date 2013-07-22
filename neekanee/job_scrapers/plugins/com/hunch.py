import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Hunch',
    'hq': 'New York, NY',

    'contact': 'jobs@hunch.com',
    'benefits': {'vacation': []},

    'home_page_url': 'http://www.hunch.com',
    'jobs_page_url': 'http://hunch.com/info/jobs/',

    'empcnt': [11,50]
}

class HunchJobScraper(JobScraper):
    def __init__(self):
        super(HunchJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='content')
        d.extract()

        self.company.job_set.all().delete()

        for h2 in d.findAll('h2'):
            job = Job(company=self.company)
            job.title = h2.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = ''

            x = h2.next
            while x and getattr(x, 'name', None) != 'h2':
                if hasattr(x, 'name') is False: 
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return HunchJobScraper()
