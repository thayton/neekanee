import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.urlutil import url_query_get

from neekanee_solr.models import *

COMPANY = {
    'name': 'LivingSocial',
    'hq': 'Washington, DC',

    'home_page_url': 'http://www.livingsocial.com',
    'jobs_page_url': 'https://jobboard.livingsocial.com/jobs/search',

    'empcnt': [1001,5000]
}

class LivingSocialJobScraper(JobScraper):
    def __init__(self):
        super(LivingSocialJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'job-link'}
        
        for a in s.findAll('a', attrs=x):
            t = a.findParent('table')
            l = self.parse_location(t.parent.h3)
            
            if not l:
                continue

            d = url_query_get(a['href'], 'deep_link')
            u = urlparse.urljoin(self.company.jobs_page_url, d['deep_link'])

            job = Job(company=self.company)
            job.title = a.text
            job.url = u
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
            b = s.html.body

            job.desc = get_all_text(b)
            job.save()

def get_scraper():
    return LivingSocialJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
