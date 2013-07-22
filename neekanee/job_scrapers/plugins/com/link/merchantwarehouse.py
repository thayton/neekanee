import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Merchant Warehouse',
    'hq': 'Boston, MA',

    'home_page_url': 'http://merchantwarehouse.com',
    'jobs_page_url': 'http://merchantwarehouse.com/employment',

    'empcnt': [51,200]
}

class MerchantWarehouseJobScraper(JobScraper):
    def __init__(self):
        super(MerchantWarehouseJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': re.compile(r'employment')}
        l = s.find('li', attrs=x)
        x = {'class': 'menu'}
        u = l.find('ul', attrs=x)

        for a in u.findAll('a'):
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
            x = {'class': re.compile(r'title')}
            h = s.find('h1', attrs=x)
            d = h.findParent('div')

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return MerchantWarehouseJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
