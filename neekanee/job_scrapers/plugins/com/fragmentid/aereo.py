import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Aereo',
    'hq': 'New York, NY',

    'home_page_url': 'https://aereo.com',
    'jobs_page_url': 'https://aereo.com/careers',

    'empcnt': [51,200]
}

class AereoJobScraper(JobScraper):
    def __init__(self):
        super(AereoJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        x = {'class': 'content'}
        d = s.find('div', attrs=x)
        x = {'class': 'col1'}
        d = d.find('div', attrs=x)
        x = {'class': 'title'}
        i = 0

        self.company.job_set.all().delete()

        for h4 in d.findAll('h4', attrs=x):
            v = h4.findNext('div', attrs={'class': 'career'})
            job = Job(company=self.company)
            job.title = h4.text
            job.url = urlparse.urljoin(self.br.geturl(), '#c%d' % i)
            job.location = self.company.location
            job.desc = get_all_text(v)
            job.save()
            i += 1

def get_scraper():
    return AereoJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
