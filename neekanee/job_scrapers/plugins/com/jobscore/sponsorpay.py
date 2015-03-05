import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'SponsorPay',
    'hq': 'Berlin, Germany',

    'home_page_url': 'http://www.sponsorpay.com',
    'jobs_page_url': 'http://www.jobscore.com/jobs/sponsorpay/',

    'empcnt': [51,200]
}

class SponsorPayJobScraper(JobScraper):
    def __init__(self):
        super(SponsorPayJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        # Rebranded to Fyber
        self.company.job_set.all().delete()

def get_scraper():
    return SponsorPayJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
