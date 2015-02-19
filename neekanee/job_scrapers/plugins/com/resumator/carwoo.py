import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'CarWoo',
    'hq': 'Burlingame, CA',

    'home_page_url': 'http://www.carwoo.com',
    'jobs_page_url': 'http://carwoo.theresumator.com',

    'empcnt': [5001,10000]
}

class CarWooJobScraper(JobScraper):
    def __init__(self):
        super(CarWooJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        # Acquired by TrueCar
        self.company.job_set.all().delete()

def get_scraper():
    return CarWooJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()

