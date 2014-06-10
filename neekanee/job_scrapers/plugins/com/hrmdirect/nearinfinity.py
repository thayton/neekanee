import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Near Infinity',
    'hq': 'Reston, VA',

    'ats': 'hrmdirect',

    'home_page_url': 'http://www.nearinfinity.com',
    'jobs_page_url': 'http://nearinfinity.hrmdirect.com/employment/openings.php',

    'gptwcom_entrepreneur': True,

    'empcnt': [51,200]
}

class NearInfinityJobScraper(JobScraper):
    def __init__(self):
        super(NearInfinityJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        # Now Altimera
        self.company.job_set.all().delete()

def get_scraper():
    return NearInfinityJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
