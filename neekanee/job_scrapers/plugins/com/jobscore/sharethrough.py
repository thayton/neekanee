import re, urlparse

from neekanee.jobscrapers.jobscore.jobscore2 import JobScoreJobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Sharethrough',
    'hq': 'San Francisco, CA',

    'ats': 'JobScore',

    'contact': 'careers@sharethrough.com',

    'home_page_url': 'http://www.sharethrough.com',
    'jobs_page_url': 'http://www.jobscore.com/jobs/sharethrough/',

    'empcnt': [11,50]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
