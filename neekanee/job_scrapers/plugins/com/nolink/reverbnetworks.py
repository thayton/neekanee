import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'ReVerb Networks',
    'hq': 'Ashburn, VA',

    'home_page_url': 'http://www.reverbnetworks.com',
    'jobs_page_url': 'http://www.reverbnetworks.com/about/careers',

    'empcnt': [11,50]
}

class ReverbNetworksJobScraper(JobScraper):
    def __init__(self):
        super(ReverbNetworksJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        d = s.find('div', id='careers')
        x = {'class': 'x-accordion-group'}

        self.company.job_set.all().delete()

        for g in d.findAll('div', attrs=x):
            job = Job(company=self.company)
            job.title = g.strong.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = get_all_text(g)
            job.save()

def get_scraper():
    return ReverbNetworksJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
