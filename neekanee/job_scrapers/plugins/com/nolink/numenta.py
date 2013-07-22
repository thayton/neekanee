import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Numenta',
    'hq': 'San Francisco, CA',

    'home_page_url': 'https://www.numenta.com',
    'jobs_page_url': 'https://www.groksolutions.com/careers.html',

    'empcnt': [11,50]
}

class NumentaJobScraper(JobScraper):
    def __init__(self):
        super(NumentaJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        t = 'Apply now'
        f = lambda x: x.text == t and x.name == 'a' and x.get('class', None) == 'button'

        self.company.job_set.all().delete()

        for a in s.findAll(f):
            d = a.parent
            v = d.findNextSibling('div')

            job = Job(company=self.company)
            job.title = d.h3.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = get_all_text(v)
            job.save()

def get_scraper():
    return NumentaJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
