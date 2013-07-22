import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Comprehend Systems',
    'hq': 'Palo Alto, CA',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.comprehend.com',
    'jobs_page_url': 'http://www.comprehend.com/careers/',

    'empcnt': [1,10]
}

class ComprehendJobScraper(JobScraper):
    def __init__(self):
        super(ComprehendJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        x = {'class': 'positions'}
        ul = s.find('ul', attrs=x)

        self.company.job_set.all().delete()

        for li in ul.findAll('li', recursive=False):
            job = Job(company=self.company)
            job.title = li.h3.text
            job.url = self.br.geturl()
            job.desc = get_all_text(li)
            job.location = self.company.location
            job.save()

def get_scraper():
    return ComprehendJobScraper()
