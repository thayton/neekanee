import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'DESY',
    'hq': 'Hamburg, Germany',

    'home_page_url': 'http://www.desy.de',
    'jobs_page_url': 'http://www.desy.de/about_desy/career/job_offers/index_eng.html',

    'empcnt': [1001,5000]
}

class DesyJobScraper(JobScraper):
    def __init__(self):
        super(DesyJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        x = {'class': 'jobDiv'}
        z = re.compile(r'\.pdf$')

        locations = { re.compile(r'Hamburg', re.I): self.parse_location('Hamburg, Germany'), 
                      re.compile(r'Zeuthen', re.I): self.parse_location('Zeuthen, Germany')}

        for d in s.findAll('div', attrs=x):
            for r,l in locations.items():
                if d.table.th is None:
                    l = None
                elif re.search(r, d.table.th.text):
                    break
                else:
                    l = None

            if not l:
                continue

            for a in d.findAll('a', href=z):
                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
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
    return DesyJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
