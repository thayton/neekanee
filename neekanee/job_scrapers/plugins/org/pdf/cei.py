import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'Competitive Enterprise Institute',
    'hq': 'Washington, DC',

    'home_page_url': 'http://www.cei.org',
    'jobs_page_url': 'http://cei.org/jobs',

    'empcnt': [11,50]
}

class CeiJobScraper(JobScraper):
    def __init__(self):
        super(CeiJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'\.pdf$')
        v = re.compile(r'job description', re.I)
        f = lambda x: x.name == 'a' and re.search(r, x.get('href', '')) and re.search(v, x.text)

        for a in s.findAll(f):
            job = Job(company=self.company)
            job.title = a.findPrevious('strong').text
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
    return CeiJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
