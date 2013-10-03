import re, urlparse, mechanize

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Cooper Power Systems',
    'hq': 'Waukesha, WI',

    'home_page_url': 'http://www.cooperpower.com',
    'jobs_page_url': 'https://cooperindustries.mua.hrdepartment.com/hrdepartment/ats/JobSearch/viewAll',

    'empcnt': [10001]
}

class CooperPowerJobScraper(JobScraper):
    def __init__(self):
        super(CooperPowerJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        # Acquired by Eaton
        self.company.job_set.all().delete()

def get_scraper():
    return CooperPowerJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
