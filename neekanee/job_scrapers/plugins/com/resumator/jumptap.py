import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Jumptap',
    'hq': 'Cambridge, MA',

    'home_page_url': 'http://www.jumptap.com',
    'jobs_page_url': 'http://jumptap.theresumator.com',

    'empcnt': [51,200]
}

class JumptapJobScraper(JobScraper):
    def __init__(self):
        super(JumptapJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        # Acquired
        self.company.job_set.all().delete()

def get_scraper():
    return JumptapJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
