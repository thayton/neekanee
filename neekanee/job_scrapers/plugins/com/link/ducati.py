import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.urlutil import url_query_add, url_query_del

from neekanee_solr.models import *

COMPANY = {
    'name': 'Ducati Motor Holding',
    'hq': 'Bologna, Italy',

    'home_page_url': 'http://www.ducati.com',
    'jobs_page_url': 'http://secure.ducati.com/Applications/ruai.nsf/$$ViewTemplate%20for%20Jobs?OpenPage&AutoFramed&BaseTarget=_self',

    'empcnt': [1001,5000]
}

class DucatiMotorHoldingJobScraper(JobScraper):
    def __init__(self):
        super(DucatiMotorHoldingJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        p = None

        pages = []
        start = 1

        while True:
            s = soupify(self.br.response().read())
            t = s.find('table', id='datiVista')
            r = re.compile(r'^\./Jobs/[A-Z0-9]+\?Open$')

            for a in t.findAll('a', href=r):
                job = Job(company=self.company)
                job.title = a.b.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = self.company.location
                jobs.append(job)
                start += 1

            n = '/Applications/ruai.nsf/$$ViewTemplate%20for%20Jobs?OpenPage&Start='+'%d' % start + '&BaseTarget=_self&AutoFramed'

            if n == p:
                break
            else:
                p = n

            u = urlparse.urljoin(self.br.geturl(), n)

            self.br.open(u)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            s = soupify(self.br.response().read())
            t = s.find('table', id='datiOfferta')

            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return DucatiMotorHoldingJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
