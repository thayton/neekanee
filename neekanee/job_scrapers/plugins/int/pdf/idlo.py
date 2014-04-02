import re, urlparse, urllib, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'International Development Law Organization',
    'hq': 'Roma, Italy',

    'home_page_url': 'http://www.idlo.int',
    'jobs_page_url': 'http://www.idlo.org/english/employment/Pages/EmploymentHome.aspx',

    'empcnt': [51,200]
}

class NatoJobScraper(JobScraper):
    def __init__(self):
        super(NatoJobScraper, self).__init__(COMPANY, return_usa_only=False)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'^ctl\d+_PlaceHolderMain_PageContent__ControlWrapper_RichHtmlField')
        d = s.find('div', id=r)
        r = re.compile(r'^/english/employment/apply/[^.]+\.aspx$')

        for a in d.findAll('a', href=r):
            u = urlparse.urljoin(self.br.geturl(), a['href'])
            self.br.open(u)

            z = soupify(self.br.response().read())
            y = re.compile(r'/DOCJob/\d+\.pdf$')
            x = {'href': r, 'target': '_blank'}

            for a in z.findAll('a', href=y):
                tr = a.findParent('tr')
                td = tr.findAll('td')
            
                l = self.parse_location(td[2].text)
                if not l:
                    continue

                job = Job(company=self.company)
                job.title = a.text
                job.url = urlparse.urljoin(self.br.geturl(), a['href'])
                job.url = job.url.encode('utf8')
                job.url = urllib.quote(job.url, '/:')
                job.location = l
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

            job.desc = get_all_text(s.html.body)
            job.save()

def get_scraper():
    return NatoJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
