import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify

from neekanee_solr.models import *

COMPANY = {
    'name': 'Bay Computer Associates',
    'hq': 'Cranston, RI',

    'home_page_url': 'http://www.baycomp.com',
    'jobs_page_url': 'https://www.baycomp.com/about/#careers',

    'empcnt': [11,50]
}

class BayCompJobScraper(JobScraper):
    def __init__(self):
        super(BayCompJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        self.company.job_set.all().delete()

def get_scraper():
    return BayCompJobScraper()
