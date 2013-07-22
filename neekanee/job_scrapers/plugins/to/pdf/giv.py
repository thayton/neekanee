import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'Giv.to',
    'hq': 'Washington, DC',

    'contact': 'mailto:rachelle@giv.to',

    'home_page_url': 'http://www.giv.to',
    'jobs_page_url': 'http://www.giv.to/about#jobs',

    'empcnt': [1,10]
}

class GivJobScraper(JobScraper):
    def __init__(self):
        super(GivJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        t = s.find('table', attrs={'class': 'image-list'})

        for td in t.tr.findAll('td'):
            job = Job(company=self.company)
            job.title = td.findAll('a')[-1].text
            job.url = urlparse.urljoin(self.br.geturl(), td.a['href'])
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
    return GivJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
