import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Elbrys Networks',
    'hq': 'Portsmouth, NH',

    'home_page_url': 'http://elbrys.com',
    'jobs_page_url': 'http://elbrys.com/?page_id=104',

    'empcnt': [11,50]
}

class ElbrysJobScraper(JobScraper):
    def __init__(self):
        super(ElbrysJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        n = s.find('section', id='content')
        x = {'class': 'toggler-wrapper'}

        self.company.job_set.all().delete()

        for v in n.findAll('div', attrs=x):
            job = Job(company=self.company)
            job.title = v.strong.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = get_all_text(v)
            job.save()

def get_scraper():
    return ElbrysJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
