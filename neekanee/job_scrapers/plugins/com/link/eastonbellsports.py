import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Easton-Bell Sports',
    'hq': 'Van Nuys, CA',

    'home_page_url': 'http://www.eastonbellsports.com',
    'jobs_page_url': 'https://www.eastonbellsports.com/careers/search/',

    'empcnt': [1001,5000]
}

class EastonBellSportsJobScraper(JobScraper):
    def __init__(self):
        super(EastonBellSportsJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        # Name change to BRG Sports
        self.company.job_set.all().delete()

def get_scraper():
    return EastonBellSportsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
