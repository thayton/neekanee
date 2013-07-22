import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Matasano Security',
    'hq': 'Chicago, IL',

    'contact': 'info@matasano.com',
    'benefits': {'vacation': []},

    'home_page_url': 'http://www.matasano.com',
    'jobs_page_url': 'http://www.matasano.com/careers/',

    'empcnt': [11,50]
}

class MatasanoJobScraper(JobScraper):
    def __init__(self):
        super(MatasanoJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        u = s.find('ul', id='secondary-content')

        self.company.job_set.all().delete()

        for h2 in u.findAll('h2'):
            ul = h2.findParent('li').ul

            job = Job(company=self.company)
            job.title = h2.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = get_all_text(ul)
            job.save()

def get_scraper():
    return MatasanoJobScraper()
