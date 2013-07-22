import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Mcgill University',
    'hq': 'Montreal, Canada',

    'home_page_url': 'http://www.mcgill.ca',
    'jobs_page_url': 'http://www.mcgill.ca/hr/workingmcgill/positions-available',

    'empcnt': [10001]
}

class McgillJobScraper(JobScraper):
    def __init__(self):
        super(McgillJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'job-title'}
        
        for p in s.findAll('p', attrs=x):
            a = p.parent.a
            job = Job(company=self.company)
            job.title = p.text
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
            d = s.find('div', id='main-column')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return McgillJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
