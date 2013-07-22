import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify

from neekanee_solr.models import *

COMPANY = {
    'name': 'Furman University',
    'hq': 'Greenville, SC',

    'benefits': {
        'url': 'http://www2.furman.edu/sites/HR/benefits/Pages/default.aspx',
        'vacation': [(0,10),(5,12),(11,15),(16,17),(21,20)],
        'holidays': 12,
        'sick_days': 10,
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.furman.edu',
    'jobs_page_url': 'http://www2.furman.edu/sites/HR/availablepositions/Pages/default.aspx',

    'gctw_chronicle': True,

    'empcnt': [501,1000]
}

class FurmanJobScraper(JobScraper):
    def __init__(self):
        super(FurmanJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='mainContentOneColumn')

        self.company.job_set.all().delete()

        for h3 in d.findAll('h3'):
            if len(h3.text) == 0 or \
                    h3.text == 'APPLICANT\'S STATEMENT':
                continue

            job = Job(company=self.company)
            job.title = h3.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = ''

            x = h3.next
            while x and getattr(x, 'name', None) != 'hr':
                if hasattr(x, 'name') is False: 
                    job.desc += x
                x = x.next

            job.save()

def get_scraper():
    return FurmanJobScraper()
