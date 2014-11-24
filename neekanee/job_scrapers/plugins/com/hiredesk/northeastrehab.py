import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Northeast Rehabilitation Network',
    'hq': 'Salem, NH',

    'home_page_url': 'http://www.northeastrehab.com',
    'jobs_page_url': 'http://careers2.hiredesk.net/Welcome/Default.asp?Comp=NorthEastRehab&AN=en-US',

    'empcnt': [501,1000]
}

class NortheastRehabJobScraper(JobScraper):
    def __init__(self):
        super(NortheastRehabJobScraper, self).__init__(COMPANY, return_usa_only=False)

    def scrape_jobs(self):
        # Site now forbids scraping
        self.company.job_set.all().delete()

def get_scraper():
    return NortheastRehabJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
