import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Ruckus Wireless',
    'hq': 'Sunnyvale, CA',

    'contact': 'jobs@ruckuswireless.com',
    'benefits': {'vacation': []},

    'home_page_url': 'http://www.ruckuswireless.com',
    'jobs_page_url': 'http://www.ruckuswireless.com/jobs/us',

    'empcnt': [201,500]
}

class RuckusWirelessJobScraper(JobScraper):
    def __init__(self):
        super(RuckusWirelessJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)
        
        s = soupify(self.br.response().read())
        x = {'class': 'job'}
        d = s.find('div', id='main')
        d.extract()

        self.company.job_set.all().delete()

        for v in d.findAll('div', attrs=x):
            x = d.find('div', attrs={'class': 'jobmeta'})
            l = self.parse_location(x.p.text)

            if l is None:
                continue

            job = Job(company=self.company)
            job.title = v.h2.text
            job.url = self.br.geturl()
            job.desc = get_all_text(v)
            job.location = l
            job.save()

def get_scraper():
    return RuckusWirelessJobScraper()
