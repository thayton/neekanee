import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto
from BeautifulSoup import BeautifulSoup, SoupStrainer

from neekanee_solr.models import *

COMPANY = {
    'name': 'Hashrocket',
    'hq': 'Jacksonville, FL',

    'contact': 'jobs@hashrocket.com',
    'benefits': {'vacation': [(1,20)]},

    'home_page_url': 'http://hashrocket.com',
    'jobs_page_url': 'http://hashrocket.com/job_applications/new',

    'empcnt': [11,50]
}

class HashRocketJobScraper(JobScraper):
    def __init__(self):
        super(HashRocketJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^/contact-us/jobs/[^/]+')

        for a in s.findAll('a', href=r):
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

            a = BeautifulSoup(self.br.response().read(), SoupStrainer('article'))

            job.desc = get_all_text(a)
            job.save()

def get_scraper():
    return HashRocketJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
