import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Lexity',
    'hq': 'Mountain View, CA',

    'home_page_url': 'http://lexity.com',
    'jobs_page_url': 'http://lexity.com/about/jobs',

    'empcnt': [11,50]
}

class VurveJobScraper(JobScraper):
    def __init__(self):
        super(VurveJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        # Lexity acquired by Yahoo
        # http://mashable.com/2013/07/31/yahoo-acquires-lexity/
        self.company.job_set.all().delete()

def get_scraper():
    return VurveJobScraper()
