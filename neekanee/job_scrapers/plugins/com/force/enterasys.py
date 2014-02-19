import re, urlparse, mechanize, urlutil

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Enterasys',
    'hq': 'Andover, MA',

    'home_page_url': 'http://www.enterasys.com',
    'jobs_page_url': 'http://enterasys.force.com/careers',

    'empcnt': [10001]
}

class EnterasysJobScraper(JobScraper):
    def __init__(self):
        super(EnterasysJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        # XXX 
        # Enterasys is now extremem networks
        self.company.job_set.all().delete()

def get_scraper():
    return EnterasysJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
