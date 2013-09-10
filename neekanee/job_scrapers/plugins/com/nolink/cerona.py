import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Cerona Networks',
    'hq': 'Frederick, MD',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.cerona.com',
    'jobs_page_url': 'http://www.cerona.com/careers.html',

    'empcnt': [11,50]
}

class CeronaJobScraper(JobScraper):
    def __init__(self):
        super(CeronaJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        # Cerona is now defunct
        self.company.job_set.all().delete()

def get_scraper():
    return CeronaJobScraper()
