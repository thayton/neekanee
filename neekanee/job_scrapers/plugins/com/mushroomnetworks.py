import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Mushroom Networks',
    'hq': 'San Diego, CA',

    'contact': 'hr@mushroomnetworks.com',
    'benefits': {'vacation': []},

    'home_page_url': 'http://www.mushroomnetworks.com',
    'jobs_page_url': 'http://www.mushroomnetworks.com/company_careers.aspx',

    'empcnt': [1,10]
}

class MushroomNetworksJobScraper(JobScraper):
    def __init__(self):
        super(MushroomNetworksJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='intro-section')
        d.extract()

        self.company.job_set.all().delete()

        for t in d.findAll('strong'):
            if not t.text:
                continue

            job = Job(company=self.company)
            job.title = t.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = ''

            x = t.next
            while x and getattr(x, 'name', None) != 'br':
                if hasattr(x, 'name') is False: 
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return MushroomNetworksJobScraper()
