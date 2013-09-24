import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'SeatMe',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.seatme.com',
    'jobs_page_url': 'http://www.seatme.com/jobs/',

    'empcnt': [1,10]
}

class SeatMeJobScraper(JobScraper):
    def __init__(self):
        super(SeatMeJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        # SeatMe acquired by Yelp
        # http://www.webpronews.com/yelp-acquires-seatme-better-online-reservations-and-more-closing-the-loop-2013-07
        self.company.job_set.all().delete()

def get_scraper():
    return SeatMeJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
