import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Transaction Network Services',
    'hq': 'Reston, VA',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.tnsi.com',
    'jobs_page_url': 'http://www.tnsi.com/why-tns/careers-at-tns',

    'empcnt': [501,1000],

    'glassdoor_eid': 313838,
    'glassdoor_rating': 2.5
}

class TnsiJobScraper(JobScraper):
    def __init__(self):
        super(TnsiJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        pass

    def scrape_jobs(self):
        pass

def get_scraper():
    return TnsiJobScraper()
