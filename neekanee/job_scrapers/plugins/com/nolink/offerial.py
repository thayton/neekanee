import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Offerial',
    'hq': 'Athens, Greece',

    'home_page_url': 'http://offerial.com',
    'jobs_page_url': 'http://offerial.com/jobs',

    'empcnt': [1,10]
}

class OfferialJobScraper(JobScraper):
    def __init__(self):
        super(OfferialJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        x = {'class': 'jobs2 content'}
        d = s.find('div', attrs=x)

        self.company.job_set.all().delete()

        for h4 in d.findAll('h4'):
            v = h4.findNext('div')
            l = self.parse_location(v.h3.nextSibling)
            
            if not l:
                continue

            job = Job(company=self.company)
            job.title = h4.text
            job.url = self.br.geturl() 
            job.location = l
            job.desc = get_all_text(v)
            job.save()

def get_scraper():
    return OfferialJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
