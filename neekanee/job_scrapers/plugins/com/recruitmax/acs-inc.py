import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'ACS',
    'hq': 'Columbia, MD',

    'ats': 'Taleo',

    'home_page_url': 'http://www.acs-inc.com',
    'jobs_page_url': 'http://www.acs-inc.com/careeropportunities.aspx',

    'empcnt': [10001]
}

class AcsIncJobScraper(JobScraper):
    def __init__(self):
        super(AcsIncJobScraper, self).__init__(COMPANY)
    def scrape_jobs(self):
        # Acquired by Xerox
        self.company.job_set.all().delete()

def get_scraper():
    return AcsIncJobScraper()
