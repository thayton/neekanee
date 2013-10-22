import re, urlparse

from neekanee.jobscrapers.jobscore.jobscore import JobScoreJobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'CareCloud',
    'hq': 'Miami, FL',

    'ats': 'Jobscore',

    'home_page_url': 'http://www.carecloud.com',
    'jobs_page_url': 'http://www.jobscore.com/jobs/carecloud/',

    'empcnt': [201,500]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
    
