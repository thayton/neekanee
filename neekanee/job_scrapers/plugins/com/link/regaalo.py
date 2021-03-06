import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Regaalo',
    'hq': 'Portsmouth, NH',

    'home_page_url': 'http://www.regaalo.com',
    'jobs_page_url': 'https://www.regaalo.com/jobs',

    'empcnt': [11,50]
}

class RegaaloJobScraper(JobScraper):
    def __init__(self):
        super(RegaaloJobScraper, self).__init__(COMPANY, return_usa_only=False)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'jobs-link'}
        d = s.find('div', attrs=x)

        for v in s.findAll('div', attrs=x):
            if v.a is None:
                continue

            job = Job(company=self.company)
            job.title = v.a.text
            job.url = urlparse.urljoin(self.br.geturl(), v.a['href'])
            job.location = self.company.location
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            try:
                self.br.open(job.url)
            except:
                continue

            s = soupify(self.br.response().read())
            x = {'class': 'main-content'}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return RegaaloJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
