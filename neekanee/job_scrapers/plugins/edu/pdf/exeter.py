import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'Phillips Exeter Academy',
    'hq': 'Exeter, NH',

    'home_page_url': 'http://www.exeter.edu',
    'jobs_page_url': 'http://www.exeter.edu/about_us/171_336.aspx',

    'empcnt': [501,1000]
}

class ExeterJobScraper(JobScraper):
    def __init__(self):
        super(ExeterJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        for t in [r'^Full-Time Positions\s*$', r'^Part-Time Positions\s*$', r'^Teaching Positions\s*$']:
            r = re.compile(t)

            try:
                self.br.follow_link(self.br.find_link(text_regex=r))
            except:
                continue
            
            s = soupify(self.br.response().read())
            r = re.compile(r'^/documents/[a-zA-Z0-9_-]+\.pdf$')
        
            for a in s.findAll('a', href=r):
                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.location = self.company.location
                jobs.append(job)

            self.br.back()

        return jobs

    def scrape_jobs(self):
        job_list = self.scrape_job_links(self.company.jobs_page_url)
        self.prune_unlisted_jobs(job_list)
        new_jobs = self.new_job_listings(job_list)

        for job in new_jobs:
            self.br.open(job.url)

            d = self.br.response().read()
            s = soupify(pdftohtml(d))

            job.desc = get_all_text(s)
            job.save()

def get_scraper():
    return ExeterJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
