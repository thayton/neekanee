import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'Demos',
    'hq': 'New York, NY',

    'benefits': {
        'vacation': [(1,20)]
    },

    'home_page_url': 'http://www.demos.org',
    'jobs_page_url': 'http://www.demos.org/job-opportunities',

    'empcnt': [11,50]
}

class DemosJobScraper(JobScraper):
    def __init__(self):
        super(DemosJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='content-area')
        x = {'name': True}
        d.extract()

        self.company.job_set.all().delete()

        for a in d.findAll('a', attrs=x):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), '#' + a['name'])
            job.location = self.company.location
            job.desc = ''

            x = a
            x = x.next

            while x:
                if getattr(x, 'name', None) == 'a' and x.name:
                    break
                if hasattr(x, 'name') is False: 
                    job.desc += x
                x = x.next
                
            job.save()

def get_scraper():
    return DemosJobScraper()
