import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'KTM',
    'hq': 'Mattighofen, Austria',

    'home_page_url': 'http://www.ktm.com',
    'jobs_page_url': 'http://company.ktm.com/gb/careers/entry-opportunities.html',

    'empcnt': [51,200],
}

class KtmJobScraper(JobScraper):
    def __init__(self):
        super(KtmJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        x = {'id': True, 'class': re.compile(r'csc-frame-accordion')}
        
        self.company.job_set.all().delete()

        for d in s.findAll('div', attrs=x):
            job = Job(company=self.company)
            job.title = d.h1.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return KtmJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
