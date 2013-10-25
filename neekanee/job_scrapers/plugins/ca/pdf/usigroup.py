import re, urlparse, copy

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.txtextract.pdftohtml import pdftohtml
from BeautifulSoup import BeautifulSoup

from neekanee_solr.models import *

COMPANY = {
    'name': 'Universal Geomatics Solutions',
    'hq': 'Edmonton, Canada',

    'home_page_url': 'http://usigroup.ca',
    'jobs_page_url': 'http://usigroup.ca/careers.html',

    'empcnt': [51,200]
}

class USIGroupJobScraper(JobScraper):
    def __init__(self):
        super(USIGroupJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        myMassage = [(re.compile(r'\\"'), lambda m: '"')]
        myNewMassage = copy.copy(BeautifulSoup.MARKUP_MASSAGE)
        myNewMassage.extend(myMassage)

        s = BeautifulSoup(self.br.response().read(), markupMassage=myNewMassage)
        r = re.compile(r'^jobs/[^.]+\.pdf$')

        for a in s.findAll('a', href=r):
            p = a.findPrevious('p')
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

            d = self.br.response().read()
            s = soupify(pdftohtml(d))

            job.desc = get_all_text(s.html.body)
            job.save()

def get_scraper():
    return USIGroupJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
