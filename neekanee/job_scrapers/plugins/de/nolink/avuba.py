import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from doctohtml import doctohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'Avuba GmbH',
    'hq': 'Berlin, Germany',

    'home_page_url': 'http://www.avuba.de',
    'jobs_page_url': 'https://www.avuba.de/#/jobs',

    'empcnt': [1,10]
}

class AvubaJobScraper(JobScraper):
    def __init__(self):
        super(AvubaJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'/document/d/')
        
        for a in s.findAll('a', href=r):
            d = a.findParent('div')
            job = Job(company=self.company)
            job.title = d.h4.text

            # URL is to a Google .doc - we update the URL so that it exports a .txt file
            # to us when we download it below
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.url = urlparse.urljoin(job.url, 'export?format=txt')

            job.location = self.company.location
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)
            job.desc = self.br.response().read()
            job.save()

def get_scraper():
    return AvubaJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
