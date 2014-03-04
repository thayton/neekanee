import os, re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Logos',
    'hq': 'Bellingham, WA',

    'home_page_url': 'http://www.logos.com',
    'jobs_page_url': 'http://www.logos.com/about/careers/',

    'empcnt': [201,500]
}

class LogosJobScraper(JobScraper):
    def __init__(self):
        super(LogosJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'/jobs/[\w-]+$')

        for a in s.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])

            if job.url.find('..') != -1:
                path = os.path.realpath(urlparse.urlparse(job.url).path)
                job.url = urlparse.urljoin(self.br.geturl(), path)

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
            d = s.find('div', id='main')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return LogosJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
