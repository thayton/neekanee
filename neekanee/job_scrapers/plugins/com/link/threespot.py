import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Threespot',
    'hq': 'Washington, DC',

    'home_page_url': 'http://www.threespot.com',
    'jobs_page_url': 'http://www.threespot.com/agency/join-us/',

    'empcnt': [51,200]
}

class ThreeSpotJobScraper(JobScraper):
    def __init__(self):
        super(ThreeSpotJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'job-open'}

        for d in s.findAll('div', attrs=x):
            job = Job(company=self.company)
            job.title = d.a.text
            job.url = urlparse.urljoin(self.br.geturl(), d.a['href'])
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
            d = s.find('div', id='content')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return ThreeSpotJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
