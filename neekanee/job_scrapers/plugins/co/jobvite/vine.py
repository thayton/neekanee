import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Vine',
    'hq': 'New York, NY',

    'home_page_url': 'https://vine.co',
    'jobs_page_url': 'https://vine.co/jobs',

    'empcnt': [11,50]
}

class VineJobScraper(JobScraper):
    def __init__(self):
        super(VineJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self, url):
        # Vine acquired by Twitter
        self.company.job_set.all().delete()

def get_scraper():
    return VineJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
