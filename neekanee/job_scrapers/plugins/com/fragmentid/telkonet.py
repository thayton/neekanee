import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'Telkonet',
    'hq': 'Milwaukee, WI',

    'home_page_url': 'http://www.telkonet.com',
    'jobs_page_url': 'http://www.telkonet.com/employment/',

    'empcnt': [51,200]
}

class TelkonetJobScraper(JobScraper):
    def __init__(self):
        super(TelkonetJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        x = {'class': 'job'}

        self.company.job_set.all().delete()

        for d in s.findAll('div', attrs=x):
            job = Job(company=self.company)
            job.title = d.a.text
            job.location = self.company.location
            job.url = urlparse.urljoin(self.br.geturl(), d.a['href'])
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return TelkonetJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
