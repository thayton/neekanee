import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Import IO',
    'hq': 'London, UK',

    'home_page_url': 'https://import.io',
    'jobs_page_url': 'https://import.io/jobs',

    'empcnt': [11,50]
}

class ImportIoJobScraper(JobScraper):
    def __init__(self):
        super(ImportIoJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'jobs'}
        u = s.find('ul', attrs=x)
        r = re.compile(r'^/jobs/[^.]+\.html$')
        
        for a in u.findAll('a', href=r):
            l = self.parse_location(a.span.text)
            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.strong.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.location = l
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            n = s.find('section', id='whyUs')

            job.desc = get_all_text(n)
            job.save()

def get_scraper():
    return ImportIoJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
