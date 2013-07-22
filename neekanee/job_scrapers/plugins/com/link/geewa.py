import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Geewa',
    'hq': 'Prague, Czech Republic',

    'home_page_url': 'http://www.geewa.com',
    'jobs_page_url': 'http://corporate.geewa.com/jobs/',

    'empcnt': [51,200]
}

class GeewaJobScraper(JobScraper):
    def __init__(self):
        super(GeewaJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'job-title'}
        
        for h in s.findAll('h2', attrs=x):
            job = Job(company=self.company)
            job.title = h.a.text
            job.url = urlparse.urljoin(self.br.geturl(), h.a['href'])
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
            r = re.compile(r'^job-\d+$')
            a = s.find('article', id=r)

            job.desc = get_all_text(a)
            job.save()

def get_scraper():
    return GeewaJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
