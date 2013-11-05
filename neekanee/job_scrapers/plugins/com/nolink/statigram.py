import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Statigram',
    'hq': 'Limoges, France',

    'home_page_url': 'http://statigr.am',
    'jobs_page_url': 'http://statigr.am/careers.php',

    'empcnt': [11,50]
}

class StatigramJobScraper(JobScraper):
    def __init__(self):
        super(StatigramJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='join-wrapper')
        x = {'class': 'one-job'}
        d.extract()

        self.company.job_set.all().delete()

        for v in d.findAll('div', attrs=x):
            job = Job(company=self.company)
            job.title = v.h2.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = get_all_text(v)
            job.save()

def get_scraper():
    return StatigramJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
