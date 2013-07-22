import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Rally',
    'hq': 'San Francisco, CA',

    'home_page_url': 'https://rally.org',
    'jobs_page_url': 'https://rally.org/corp/careers',

    'empcnt': [11,50]
}

class RallyJobScraper(JobScraper):
    def __init__(self):
        super(RallyJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='careers')
        x = {'class': 'job'}

        self.company.job_set.all().delete()

        for v in d.findAll('div', attrs=x):
            job = Job(company=self.company)
            job.title = v.h3 and v.h3.text or v.h2.text
            job.url = urlparse.urljoin(self.br.geturl(), v.a['href'])
            job.location = self.company.location
            job.desc = get_all_text(v)
            job.save()

def get_scraper():
    return RallyJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
