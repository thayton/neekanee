import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Meraki',
    'hq': 'San Francisco, CA',

    'benefits': {'vacation': []},

    'home_page_url': 'http://meraki.com',
    'jobs_page_url': 'http://meraki.com/company/jobs',

    'empcnt': [51,200]
}

class MerakiJobScraper(JobScraper):
    def __init__(self):
        super(MerakiJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        n = s.find('section', id='positions')
        x = {'class': re.compile(r'job-position\s'), 'data-tab': True }

        self.company.job_set.all().delete()

        for d in n.findAll('div', attrs=x):
            if d['data-tab'] == 'intro':
                continue

            job = Job(company=self.company)
            job.title = d.h3.text
            job.url = self.br.geturl()
            job.desc = get_all_text(d)
            job.location = self.company.location
            job.save()

def get_scraper():
    return MerakiJobScraper()
