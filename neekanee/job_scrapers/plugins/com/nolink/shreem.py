import re

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Shreem',
    'hq': 'Sterling, VA',

    'home_page_url': 'http://www.shreem.com',
    'jobs_page_url': 'http://www.shreem.com/open_positions.htm',

    'empcnt': [11,50]
}

class ShreemJobScraper(JobScraper):
    def __init__(self):
        super(ShreemJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        # Company has gone under / site is no longer there
        self.company.job_set.all().delete()

def get_scraper():
    return ShreemJobScraper()
