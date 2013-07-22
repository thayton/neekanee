import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'Vecima',
    'hq': 'Saskatoon, SK, Canada',

    'contact': 'human.resources@vecima.com',

    'home_page_url': 'http://www.vecima.com',
    'jobs_page_url': 'http://www.vecima.com/careers.php',

    'empcnt': [501,1000],
}

class VecimaJobScraper(JobScraper):
    def __init__(self):
        super(VecimaJobScraper, self).__init__(COMPANY, return_usa_only=False)

    def scrape_job_links(self, url):
        jobs = []

        self.br.open(url)

        s = soupify(self.br.response().read())
        f = lambda x: x.name == 'h2' and x.text == 'Current Opportunities'
        h = s.find(f)
        d = h.findParent('div')
        r = re.compile(r'/careers/\S+\.pdf$')
    
        for a in d.findAll('a', href=r):
            x = a.text.split('-')
            l = None

            if len(x) > 1:
                l = self.parse_location(x[1])

            if l is None:
                continue

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
    return VecimaJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
