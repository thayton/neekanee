import re, urllib, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'Queens University of Charlotte',
    'hq': 'Charlotte, NC',

    'home_page_url': 'http://www.queens.edu',
    'jobs_page_url': 'http://www.queens.edu/News-and-Information/Careers-at-Queens/Available-Positions.html',

    'empcnt': [201,500]
}

class QueensJobScraper(JobScraper):
    def __init__(self):
        super(QueensJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='content')
        r = re.compile(r'^Documents/HR/\d+--.*\.pdf$')

        for a in d.findAll('a', href=r):
            link = urllib.quote(urllib.unquote(a['href']), safe='/:')
            job = Job(company=self.company)
            job.title = a.text
            job.url = urlparse.urljoin(self.company.home_page_url, link)
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
    return QueensJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
