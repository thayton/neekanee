import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Central Texas College',
    'hq': 'Killeen, TX',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.ctcd.edu',
    'jobs_page_url': 'http://www.ctcd.edu/jobs/jobs_sort_date.asp',
    
    'gctw_chronicle': True,

    'empcnt': [1001,5000]
}

class CtcdJobScraper(JobScraper):
    def __init__(self):
        super(CtcdJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.br.open(self.company.jobs_page_url)

        s = soupify(self.br.response().read())
        a = { 'class': 'job_font' }

        self.company.job_set.all().delete()

        for t in s.findAll('table', attrs=a):
            job = Job(company=self.company)
            job.title = t.tr.font.text
            job.url = self.br.geturl()
            job.location = self.company.location
            job.desc = get_all_text(t)
            job.save()

def get_scraper():
    return CtcdJobScraper()

