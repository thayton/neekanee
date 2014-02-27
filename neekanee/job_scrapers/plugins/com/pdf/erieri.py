import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'ERI Economic Research Institute',
    'hq': 'Redmond, WA',

    'home_page_url': 'http://www.erieri.com',
    'jobs_page_url': 'http://www.erieri.com/index.cfm?FuseAction=Home.Careers',

    'empcnt': [51,200],
}

class EriJobScraper(JobScraper):
    def __init__(self):
        super(EriJobScraper, self).__init__(COMPANY)
        
    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        r = re.compile(r'/PDF/careers-[\w-]+\.pdf$')
        f = lambda x: x.name == 'h2' and x.text == 'Positions Available'
        h = s.find(f)
        t = h.findNext('table')
        t.extract()
    
        for h3 in t.findAll('h3'):
            l = self.parse_location(h3.text)

            if not l:
                continue

            ns = h3.nextSibling.nextSibling
            if ns.name != 'ul':
                continue
            else:
                ul = ns

            for a in ul.findAll('a', href=r):
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
    return EriJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
