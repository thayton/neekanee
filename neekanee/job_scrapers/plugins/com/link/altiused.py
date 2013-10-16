import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Altius Education',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.altiused.com',
    'jobs_page_url': 'http://www.altiused.com/jobs/available-positions',

    'empcnt': [11,50]
}

class AltiusEdJobScraper(JobScraper):
    def __init__(self):
        super(AltiusEdJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        # Acquired
        self.company.job_set.all().delete()

def get_scraper():
    return AltiusEdJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
