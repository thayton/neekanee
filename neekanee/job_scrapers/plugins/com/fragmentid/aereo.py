import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Aereo',
    'hq': 'New York, NY',

    'home_page_url': 'https://aereo.com',
    'jobs_page_url': 'https://aereo.com/careers',

    'empcnt': [51,200]
}

class AereoJobScraper(JobScraper):
    def __init__(self):
        super(AereoJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        # Out of business
        self.company.job_set.all().delete()


def get_scraper():
    return AereoJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
