import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'YouNoodle',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.younoodle.com',
    'jobs_page_url': 'http://www.younoodle.com/jobs',

    'empcnt': [11,50]
}

class YouNoodleJobScraper(JobScraper):
    def __init__(self):
        super(YouNoodleJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        x = {'class': 'static-section'}

        self.company.job_set.all().delete()

        for h1 in s.findAll('h1'):
            n = h1.nextSibling.nextSibling
            if h1.findNextSibling('div', attrs=x) != n:
                continue

            job = Job(company=self.company)
            job.title = h1.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = get_all_text(n)
            job.save()

def get_scraper():
    return YouNoodleJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
