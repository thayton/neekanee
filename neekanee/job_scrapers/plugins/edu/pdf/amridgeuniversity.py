import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'Amridge University',
    'hq': 'Montgomery, AL',

    'home_page_url': 'http://www.amridgeuniversity.edu',
    'jobs_page_url': 'http://www.amridgeuniversity.edu/careers.html',

    'empcnt': [51,200]
}

class AmridgeJobScraper(JobScraper):
    def __init__(self):
        super(AmridgeJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'pdf/Jobs/.*\.pdf$')

        for a in s.findAll('a', href=r):
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

            data = self.br.response().read()
            s = soupify(pdftohtml(data))

            job.desc = get_all_text(s.html.body)
            job.save()

def get_scraper():
    return AmridgeJobScraper()
