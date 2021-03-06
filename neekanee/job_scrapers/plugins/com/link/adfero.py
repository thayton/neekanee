import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Adfero',
    'hq': 'Washington, DC',

    'home_page_url': 'http://www.adfero.com',
    'jobs_page_url': 'http://www.adfero.com/careers/all',

    'empcnt': [11,50]
}

class AdferoJobScraper(JobScraper):
    def __init__(self):
        super(AdferoJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'/careers/[^/]+$')
        f = lambda x: x.name == 'a' and re.search(r, x.get('href', '')) and x.parent.name == 'h4'

        for a in s.findAll(f):
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
            r = re.compile(r'^node-\d+$')
            x = {'id': r}
            a = s.find('article', attrs=x)

            job.desc = get_all_text(a)
            job.save()

def get_scraper():
    return AdferoJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
