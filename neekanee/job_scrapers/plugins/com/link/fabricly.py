import re, urlparse, webcli

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Fabricly',
    'hq': 'New York, NY',

    'home_page_url': 'http://www.fabricly.com',
    'jobs_page_url': 'http://www.fabricly.com/vacancies',

    'empcnt': [1,10]
}

class FabriclyJobScraper(JobScraper):
    def __init__(self):
        super(FabriclyJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        # Fabricly closed down
        self.company.job_set.all().delete()

def get_scraper():
    return FabriclyJobScraper()
