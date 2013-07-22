import re, urlparse, urllib

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.txtextract.pdftohtml import pdftohtml
from posixpath import normpath

from neekanee_solr.models import *

COMPANY = {
    'name': 'Nucsafe',
    'hq': 'Oak Ridge, TN',

    'home_page_url': 'http://www.nucsafe.com',
    'jobs_page_url': 'http://www.nucsafe.com/cms/Employment/4.html',

    'empcnt': [51,200]
}

class NucSafeJobScraper(JobScraper):
    def __init__(self):
        super(NucSafeJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        t = s.find('table', id='tblMain')
        r = re.compile(r'/pdf/HR/.*\.pdf$')

        for a in t.findAll('a', href=r):
            if not a.br:
                continue

            job = Job(company=self.company)
            job.title = a.text

            u = urlparse.urljoin(self.br.geturl(), a['href'])
            p = urlparse.urlparse(u)
            l = list(p)
            p = normpath(p.path)
            l[2] = p

            job.url = urlparse.urlunparse(l)
            job.url = urllib.quote(job.url, ':/')
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
    return NucSafeJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
