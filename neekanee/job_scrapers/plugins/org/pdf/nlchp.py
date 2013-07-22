import re, urlparse, urllib

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'The National Law Center on Homelessness & Poverty',
    'hq': 'Washington, DC',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.nlchp.org',
    'jobs_page_url': 'http://www.nlchp.org/employment.cfm',

    'empcnt': [11,50]
}

class NlchpJobScraper(JobScraper):
    def __init__(self):
        super(NlchpJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='page_wrapper')
        r = re.compile(r'/content/pubs/.*?\.pdf$')

        for a in s.findAll('a', href=r):
            if len(a.text) == 0:
                continue

            g = a.findPrevious('strong')

            job = Job(company=self.company)
            job.title = g.text
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

            d = self.br.response().read()
            s = soupify(pdftohtml(d))

            job.desc = get_all_text(s.html.body)
            job.save()

def get_scraper():
    return NlchpJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
