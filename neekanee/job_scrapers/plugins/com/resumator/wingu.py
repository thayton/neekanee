import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Wingu',
    'hq': 'Cambridge, MA',

    'home_page_url': 'http://www.wingu.com',
    'jobs_page_url': 'http://wingu.theresumator.com',

    'empcnt': [11,50]
}

class WinguJobScraper(JobScraper):
    def __init__(self):
        super(WinguJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        # Acquired
        self.company.job_set.all().delete()

def get_scraper():
    return WinguJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
