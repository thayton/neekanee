import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'Chicago History',
    'hq': 'Chicago, IL',

    'home_page_url': 'http://www.chicagohistory.org',
    'jobs_page_url': 'http://www.chicagohistory.org/aboutus/jobsvolunteering/jobopportunities',

    'empcnt': [51,200]
}

class ChicagoHistoryJobScraper(JobScraper):
    def __init__(self):
        super(ChicagoHistoryJobScraper, self).__init__(COMPANY)
        
    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        d = s.find('div', id=re.compile(r'parent-fieldname-text'))
        r = re.compile(r'/documents/home/aboutus/jobs-and-volunteering/jobs/.*\.pdf$')

        for a in d.findAll('a', href=r):
            if len(a.text.strip()) == 0:
                continue

            h2 = a.findPrevious('h2')

            job = Job(company=self.company)
            job.title = h2.text
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
    return ChicagoHistoryJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
