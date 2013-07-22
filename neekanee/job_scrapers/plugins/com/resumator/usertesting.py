from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'UserTesting',
    'hq': 'Mountain View, CA',

    'home_page_url': 'http://www.usertesting.com',
    'jobs_page_url': 'http://usertesting.theresumator.com',

    'empcnt': [11,50]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
