import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Semphonic',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.semphonic.com',
    'jobs_page_url': 'http://www.semphonic.com/about/careers/index.aspx',

    'empcnt': [11,50]
}

class SemphonicJobScraper(JobScraper):
    def __init__(self):
        super(SemphonicJobScraper, self).__init__(COMPANY)

    def scrape_job_links(self, url):
        # Semphonic acquired by Ernst & Young
        self.company.job_set.all().delete()

def get_scraper():
    return SemphonicJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
