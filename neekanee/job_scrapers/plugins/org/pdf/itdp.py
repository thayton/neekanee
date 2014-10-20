import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'Institute for Transportation & Development Policy',
    'hq': 'New York, NY',

    'home_page_url': 'http://www.itdp.org',
    'jobs_page_url': 'https://www.itdp.org/who-we-are/jobs/',

    'empcnt': [11,50]
}

class ItdpJobScraper(JobScraper):
    def __init__(self):
        super(ItdpJobScraper, self).__init__(COMPANY)
        self.br.addheaders = [('User-agent', 
                               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7')]

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'/uploads/[^\.]+\.pdf$')
        x = {'font-weight': 'bold;'}

        for a in s.findAll('a', href=r):
            p = a.findPrevious('span')
            h = a.findPrevious('h3')

            m = re.search(re.compile(r'\(([^)]+)'), p.text)
            if m:
                l = m.group(1) + ', ' + h.text
                l = self.parse_location(l)
                if not l:
                    continue

            job = Job(company=self.company)
            job.title = p.text
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
    return ItdpJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
