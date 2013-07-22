import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'NGEN',
    'hq': 'Largo, MD',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.ngen.com',
    'jobs_page_url': 'http://www.ngen.com/employment.shtml',

    'empcnt': [11,50]
}

class NgenJobScraper(JobScraper):
    def __init__(self):
        super(NgenJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='mainbody')
        x = { 'class': 'int' }

        for p in d.findAll('p', attrs=x):
            title = p.a.text.strip().lower()
            if title.startswith('click here'):
                continue

            job = Job(company=self.company)
            job.title = p.a.text
            job.url = urlparse.urljoin(self.br.geturl(), p.a['href'])
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
    return NgenJobScraper()
