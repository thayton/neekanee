import re, urllib, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'Canisius College',
    'hq': 'Buffalo, NY',

    'home_page_url': 'http://www.canisius.edu',
    'jobs_page_url': 'http://www.canisius.edu/hr/employment/',

    'empcnt': [501,1000]
}

class CanisiusJobScraper(JobScraper):
    def __init__(self):
        super(CanisiusJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='main-content')
        r = re.compile(r'^/dotAsset/[a-z0-9-]+.*\.pdf$')

        for a in d.findAll('a', href=r):
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), urllib.quote(a['href']))
            job.location = self.company.location
            jobs.append(job)

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            d = self.br.response().read()
            s = soupify(pdftohtml(d))

            job.desc = get_all_text(s.html.body)
            job.save()

def get_scraper():
    return CanisiusJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
