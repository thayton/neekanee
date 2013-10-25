import re, urlparse, urllib

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'North American Treaty Organization (NATO)',
    'hq': 'Geneva, Switzerland',

    'home_page_url': 'http://www.nato.int',
    'jobs_page_url': 'http://www.nato.int/cps/en/natolive/recruit-wide.htm',

    'empcnt': [1001,5000]
}

class NatoJobScraper(JobScraper):
    def __init__(self):
        super(NatoJobScraper, self).__init__(COMPANY)
        # Server is determined to return gzip no matter the accept-encoding we send
        self.br.set_handle_gzip(True) 

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        t = s.find('table', id='tablesorterID')
        r = re.compile(r'/recruit/documents/.*\.pdf$')

        for a in t.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')
            
            l = self.parse_location(td[0].text)
            if not l:
                continue

            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.br.geturl(), a['href'])
            job.url = job.url.encode('utf8')
            job.url = urllib.quote(job.url, '/:')
            job.location = l
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
    return NatoJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
