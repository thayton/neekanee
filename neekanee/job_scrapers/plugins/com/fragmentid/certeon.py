import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Certeon',
    'hq': 'Burlington, MA',

    'contact': 'careers@certeon.com',
    'benefits': {'vacation': []},

    'home_page_url': 'http://www.certeon.com',
    'jobs_page_url': 'http://www.certeon.com/about-careers.aspx',

    'empcnt': [51,200]
}

class CerteonJobScraper(JobScraper):
    def __init__(self):
        super(CerteonJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', attrs={'class': 'main'})
        h = d.find('h1', attrs={'class': 'page-title'})
        d = h.findNext('div')
        x = {'style': True}
        d.extract()

        self.company.job_set.all().delete()

        for h3 in d.findAll('h3', attrs=x):
            job = Job(company=self.company)
            job.title = h3.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = ''

            x = h3.next

            while x and getattr(x, 'name', None) != 'h3':
                if hasattr(x, 'name') is False: 
                    job.desc += x
                x = x.next

            job.save()


def get_scraper():
    return CerteonJobScraper()
