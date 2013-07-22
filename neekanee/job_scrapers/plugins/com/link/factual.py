import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Factual',
    'hq': 'Los Angeles, CA',

    'home_page_url': 'http://www.factual.com',
    'jobs_page_url': 'http://www.factual.com/jobs/open-positions',

    'empcnt': [11,50]
}

class FactualJobScraper(JobScraper):
    def __init__(self):
        super(FactualJobScraper, self).__init__(COMPANY)
        self.geocoder.return_usa_only = False

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = re.compile(r'job-list')
        y = {'class': 'jobs-by-location'}
        d = s.find('div', attrs={'class': x})
        r = re.compile(r'^/jobs/\S+')

        for a in d.findAll('a', href=r):
            p = a.findParent('div', attrs=y)
            l = self.parse_location(p.h6.text)

            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.text
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
            r = re.compile(r'job-position')
            d = s.find('div', attrs={'class': r})

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return FactualJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
