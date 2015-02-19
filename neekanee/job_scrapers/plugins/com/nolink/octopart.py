import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from BeautifulSoup import BeautifulSoup

from neekanee_solr.models import *

COMPANY = {
    'name': 'Octopart',
    'hq': 'New York, NY',

    'home_page_url': 'http://octopart.com',
    'jobs_page_url': 'https://octopart.com/jobs',

    'empcnt': [11,50]
}

class OctopartJobScraper(JobScraper):
    def __init__(self):
        super(OctopartJobScraper, self).__init__(COMPANY)
        self.br.addheaders = [('User-agent', 
                               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7')]

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        # HTML is broken - skipped past to just the <body>
        d = self.br.response().read()
        i = d.find('<body')
        s = soupify(d[i:])

        x = {'class': 'positions'}
        n = s.find('section', attrs=x)
        x = {'class': 'row position'}

        self.company.job_set.all().delete()

        for d in n.findAll('div', attrs=x):
            job = Job(company=self.company)
            job.title = d.h3.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return OctopartJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()

