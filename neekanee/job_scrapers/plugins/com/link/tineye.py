import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'TinEye',
    'hq': 'Toronto, Canada',

    'home_page_url': 'http://tineye.com',
    'jobs_page_url': 'http://tineye.com/careers',

    'empcnt': [11,50]
}

class TinEyeJobScraper(JobScraper):
    def __init__(self):
        super(TinEyeJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        f = lambda x: x.name == 'strong' and x.text == 'We are currently hiring for:'
        g = s.find(f)
        ul = g.findNext('ul')

        for a in ul.findAll('a'):
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
            d = s.find('div', id='left-column')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return TinEyeJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
