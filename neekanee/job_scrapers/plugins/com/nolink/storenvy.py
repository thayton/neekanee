import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Storenvy',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.storenvy.com',
    'jobs_page_url': 'http://www.storenvy.com/jobs',

    'empcnt': [1,10]
}

class StorEnvyJobScraper(JobScraper):
    def __init__(self):
        super(StorEnvyJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        jobs = []

        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='job-openings')
        x = {'class': 'job-listing'}
        y = {'name': True}

        self.company.job_set.all().delete()

        for v in d.findAll('div', attrs=x):
            a = v.findPrevious('a', attrs=y)
            
            job = Job(company=self.company)
            job.title = v.text
            job.url = urlparse.urljoin(self.br.geturl(), a['name'])
            job.location = self.company.location
            job.desc = get_all_text(v)
            job.save()

def get_scraper():
    return StorEnvyJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
