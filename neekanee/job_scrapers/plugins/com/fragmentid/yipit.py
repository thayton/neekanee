import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'yipit',
    'hq': 'New York, NY',

    'home_page_url': 'http://yipit.com',
    'jobs_page_url': 'http://yipit.com/jobs/',

    'empcnt': [11,50]
}

class YipitJobScraper(JobScraper):
    def __init__(self):
        super(YipitJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        x = {'class': 'job'}

        self.company.job_set.all().delete()

        for n in s.findAll('section', attrs=x):
            job = Job(company=self.company)
            job.title = n.h4.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = get_all_text(n)
            job.save()

def get_scraper():
    return YipitJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
