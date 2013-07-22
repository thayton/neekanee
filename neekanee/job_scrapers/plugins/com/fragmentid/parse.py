import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Parse',
    'hq': 'San Francisco, CA',

    'home_page_url': 'https://parse.com',
    'jobs_page_url': 'https://parse.com/jobs',

    'empcnt': [11,50]
}

class ParseJobScraper(JobScraper):
    def __init__(self):
        super(ParseJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        x = {'class': 'job'}

        self.company.job_set.all().delete()

        for d in s.findAll('div', attrs=x):
            if not d.get('id', None):
                id = d.a['name']
            else:
                id = d['id']

            job = Job(company=self.company)
            job.title = d.h2.text
            job.url = urlparse.urljoin(self.br.geturl(), '#' + id)
            job.location = self.company.location
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return ParseJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
