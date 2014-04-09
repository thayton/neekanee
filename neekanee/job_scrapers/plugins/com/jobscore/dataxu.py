import re, urlparse

from neekanee.jobscrapers.jobscore.jobscore2 import JobScoreJobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'DataXu',
    'hq': 'Boston, MA',

    'ats': 'Jobscore',

    'home_page_url': 'http://www.dataxu.com',
    'jobs_page_url': 'http://www.jobscore.com/jobs/dataxu/',

    'empcnt': [11,50]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)
    
