import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Hunch',
    'hq': 'New York, NY',

    'home_page_url': 'http://www.hunch.com',
    'jobs_page_url': 'http://hunch.com/info/jobs/',

    'empcnt': [11,50]
}

class HunchJobScraper(JobScraper):
    def __init__(self):
        super(HunchJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        ''' Acquired by eBay '''
        self.company.job_set.all().delete()

def get_scraper():
    return HunchJobScraper()
