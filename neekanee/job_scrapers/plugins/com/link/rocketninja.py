import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Rocket Ninja',
    'hq': 'San Francisco, CA',

    'contact': 'Jobs@rocketninja.com',
    'benefits': {'vacation': []},

    'home_page_url': 'http://www.rocketninja.com',
    'jobs_page_url': 'http://www.rocketninja.com/Home/Join.aspx',

    'empcnt': [11,50]
}

class RocketNinjaJobScraper(JobScraper):
    def __init__(self):
        super(RocketNinjaJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        # Company appears to be gone/dead
        self.company.job_set.all().delete()

def get_scraper():
    return RocketNinjaJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
