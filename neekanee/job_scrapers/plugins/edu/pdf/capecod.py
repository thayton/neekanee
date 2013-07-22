import re, urlparse, urllib

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.urlutil import url_params_del
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'Cape Cod Community College',
    'hq': 'West Barnstable, MA',

    'home_page_url': 'http://www.capecod.edu',
    'jobs_page_url': 'http://www.capecod.edu/web/hr/jobs',

    'empcnt': [201,500]
}

class CapeCodJobScraper(JobScraper):
    def __init__(self):
        super(CapeCodJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='main-content')
        r = re.compile(r'/web/hr/jobs')

        for a in d.findAll('a', href=r):
            u = urlparse.urljoin(self.br.geturl(), a['href'])

            self.br.open(u)
            
            s = soupify(self.br.response().read())
            v = s.find('div', id='main-content')
            x = re.compile(r'document_library/get_file\?uuid=')
            a = v.find('a', href=x)

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

            d = self.br.response().read()
            s = soupify(pdftohtml(d))

            job.desc = get_all_text(s.html.body)
            job.save()

def get_scraper():
    return CapeCodJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
