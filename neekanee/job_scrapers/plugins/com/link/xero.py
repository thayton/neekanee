import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Xero',
    'hq': 'Wellington, New Zealand',

    'home_page_url': 'http://www.xero.com',
    'jobs_page_url': 'http://www.xero.com/about/careers/',

    'empcnt': [201,500]
}

class XeroJobScraper(JobScraper):
    def __init__(self):
        super(XeroJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='openings')
        r = re.compile(r'^/about/careers/job/\d+$')
        x = {'class': 'location'}

        for a in d.findAll('a', href=r):
            v = a.findParent('div')
            p = v.find('span', attrs=x)
            l = self.parse_location(p.text)
            
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
            x = {'class': 'contentWrapper'}
            d = s.find('div', attrs=x)

            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return XeroJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
