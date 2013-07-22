import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'UNESCO',
    'hq': 'Paris, France',

    'home_page_url': 'http://www.unesco.org',
    'jobs_page_url': 'https://recrutweb.unesco.org/postes/postes_visualisation.asp?AffLangue=gb&CATPOSTE=1',

    'empcnt': [1001,5000]
}

class UnescoJobScraper(JobScraper):
    def __init__(self):
        super(UnescoJobScraper, self).__init__(COMPANY, return_usa_only=False)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        t = s.findAll('table')[1]
        r = re.compile(r'/pdf/\S+\.PDF$')

        for a in t.findAll('a', href=r):
            tr = a.findParent('tr')
            td = tr.findAll('td')

            l = self.parse_location(td[-4].text)
            if not l:
                continue

            job = Job(company=self.company)
            job.title = td[0].text
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
    return UnescoJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
