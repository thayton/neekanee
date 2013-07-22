import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'PureWow',
    'hq': 'New York, NY',

    'home_page_url': 'http://www.purewow.com',
    'jobs_page_url': 'http://www.purewow.com/jobs.htm',

    'empcnt': [1,10]
}

class PureWowJobScraper(JobScraper):
    def __init__(self):
        super(PureWowJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        x = {'class': 'jobs-container'}
        y = {'class': 'slide-jobs'}
        d = s.find('div', attrs=x)

        for j in d.findAll('div', attrs=y):
            job = Job(company=self.company)
            job.title = j.a.text
            job.location = self.company.location
            job.url = self.br.geturl()
            job.desc = get_all_text(j)
            job.save()

def get_scraper():
    return PureWowJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
