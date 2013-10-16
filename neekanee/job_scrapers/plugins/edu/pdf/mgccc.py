import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'Mississippi Gulf Coast Community College',
    'hq': 'Perkinston, MS',

    'benefits': {
        'url': 'http://www.mgccc.edu/Documents/HR/BENEFITS_PACKAGE.pdf',
        'vacation': [(1,10),(4,13),(9,18),(16,19)]
    },

    'home_page_url': 'http://www.mgccc.edu',
    'jobs_page_url': 'https://www.mgccc.edu/employees/employment-opportunities/',

    'empcnt': [501,1000]
}

class MgccJobScraper(JobScraper):
    def __init__(self):
        super(MgccJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'/wp-content/uploads/\d{4}/\d{2}/\S+\.pdf$')
        x = {'title': True, 'href': r}

        for a in s.findAll('a', attrs=x):
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
    return MgccJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
