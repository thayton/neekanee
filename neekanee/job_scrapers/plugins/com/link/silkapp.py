import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Silk',
    'hq': 'Amsterdam, Netherlands',

    'home_page_url': 'http://www.silkapp.com',
    'jobs_page_url': 'http://jobs.silkapp.com/tag/position',

    'empcnt': [11,50]
}

class SilkJobScraper(JobScraper):
    def __init__(self):
        super(SilkJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        f = lambda x: x.name == 'div' and x.text == 'Document'
        d = s.find(f)
        t = d.findParent('table')

        for a in t.findAll('a'):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = self.company.location
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            d = s.find('div', id='canvas')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return SilkJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
