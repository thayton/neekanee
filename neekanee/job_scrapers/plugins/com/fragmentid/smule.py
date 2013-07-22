import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Smule',
    'hq': 'Palo Alto, CA',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.smule.com',
    'jobs_page_url': 'http://www.smule.com/jobs',

    'empcnt': [11,50]
}

class SmuleJobScraper(JobScraper):
    def __init__(self):
        super(SmuleJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^#')
        d = s.find('div', id='page-inner')
        d.extract()

        self.company.job_set.all().delete()

        for a in d.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            job.desc = ''

            x = d.find(attrs={'name' : a['href'][1:]})
            
            while x and (getattr(x, 'name', None) != 'hr' and\
                         getattr(x, 'name', None) != 'div'):
                if hasattr(x, 'name') is False: 
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return SmuleJobScraper()
