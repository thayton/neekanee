import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'Acadia Optronics, LLC',
    'hq': 'Rockville, MD',

    'home_page_url': 'http://www.acadiaoptronics.com',
    'jobs_page_url': 'http://www.acadiaoptronics.com/careers',

    'empcnt': [1,10],
}

class AcadiaOptronicsJobScraper(JobScraper):
    def __init__(self):
        super(AcadiaOptronicsJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        def select_link(link):
            if link.tag == 'iframe':
                d = dict(link.attrs)
                return d.get('title', None) == 'Acadia Careers'

            return False

        self.br.open(url)
        self.br.follow_link(self.br.find_link(predicate=select_link))

        s = soupify(self.br.response().read())
        r = re.compile(r'googledrive\S+\.pdf$')
    
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

            d = self.br.response().read()
            s = soupify(pdftohtml(d))

            job.desc = get_all_text(s.html.body)
            job.save()

def get_scraper():
    return AcadiaOptronicsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
