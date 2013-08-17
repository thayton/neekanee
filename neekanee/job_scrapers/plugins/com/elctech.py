import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'ELC',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.elctech.com',
    'jobs_page_url': 'http://elctech.com/careers',

    'empcnt': [11,50]
}

class ElcJobScraper(JobScraper):
    def __init__(self):
        super(ElcJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        # XXX ELC is now Burnside Digital 
        pass

def get_scraper():
    return ElcJobScraper()
