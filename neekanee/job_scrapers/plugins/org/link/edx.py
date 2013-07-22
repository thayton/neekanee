import re, urlparse
from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'edX',
    'hq': 'Cambridge, MA',

    'home_page_url': 'https://www.edx.org',
    'jobs_page_url': 'https://www.edx.org/jobs',

    'empcnt': [51,200]
}

class EdXJobScraper(JobScraper):
    def __init__(self):
        super(EdXJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        x = {'class': 'openposition-link'}
        
        for d in s.findAll('div', attrs=x):
            job = Job(company=self.company)
            job.title = d.parent.h3.text
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
            x = {'class': 'openposition-view'}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return EdXJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
