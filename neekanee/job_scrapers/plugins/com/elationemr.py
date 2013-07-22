import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'ElationEMR',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.elationemr.com',
    'jobs_page_url': 'http://www.elationemr.com/jobs/',

    'empcnt': [1,10]
}

class ElationEmrJobScraper(JobScraper):
    def __init__(self):
        super(ElationEmrJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        x = { 'class': re.compile(r'jobWrapper')}

        self.company.job_set.all().delete()

        for d in s.findAll('div', attrs=x):
            if d.h4 is None:
                continue

            job = Job(company=self.company)
            job.title = d.h4.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = get_all_text(d)
            job.save()

def get_scraper():
    return ElationEmrJobScraper()
