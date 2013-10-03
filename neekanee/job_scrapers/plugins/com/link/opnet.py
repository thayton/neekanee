import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'OPNET',
    'hq': 'Bethesda, MD',

    'home_page_url': 'http://www.opnet.com',
    'jobs_page_url': 'https://enterprise1.opnet.com/recruiting/positions/list_jobs',

    'empcnt': [501,1000]
}

class OpnetJobScraper(JobScraper):
    def __init__(self):
        super(OpnetJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        # Acquired by Riverbed
        self.company.job_set.all().delete()

def get_scraper():
    return OpnetJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
