import re, urlparse
from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Soundrop',
    'hq': 'Oslow, Norway',

    'home_page_url': 'http://soundrop.fm',
    'jobs_page_url': 'http://soundrop.fm/jobs',

    'empcnt': [11,50]
}

class SoundropJobScraper(JobScraper):
    def __init__(self):
        super(SoundropJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        # OOB
        self.company.job_set.all().delete()

def get_scraper():
    return SoundropJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
