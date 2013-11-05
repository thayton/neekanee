import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'TECKpert',
    'hq': 'Coral Gables, FL',

    'home_page_url': 'http://teckpert.com',
    'jobs_page_url': 'http://teckpert.com/who-we-are/careers/open-positions/',

    'empcnt': [1,10]
}

class TECKpertJobScraper(JobScraper):
    def __init__(self):
        super(TECKpertJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'/job/[^/]+/$')
        n = s.find('section', id='careers-positions-page')

        for a in n.findAll('a', href=r):
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
            x = {'class': 'static'}
            n = s.find('section', attrs=x)

            job.desc = get_all_text(n)
            job.save()

def get_scraper():
    return TECKpertJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
