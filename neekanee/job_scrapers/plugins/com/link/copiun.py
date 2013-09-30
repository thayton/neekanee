import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Copiun',
    'hq': 'Marlborough, MA',

    'home_page_url': 'http://www.copiun.com',
    'jobs_page_url': 'http://www.copiun.com/about-us/careers/',

    'empcnt': [1,10]
}

class CopiunJobScraper(JobScraper):
    def __init__(self):
        super(CopiunJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        # Copiun acquired
        # http://bostinno.streetwise.co/2012/09/05/secure-file-sharing-solution-copiun-acquired-by-good-technology/
        self.company.job_set.all().delete()

def get_scraper():
    return CopiunJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
