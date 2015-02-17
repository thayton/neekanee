import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'SpeakerText',
    'hq': 'San Francisco, CA',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.speakertext.com',
    'jobs_page_url': 'http://www.speakertext.com/jobs',

    'empcnt': [1,10]
}

class SpeakerTextJobScraper(JobScraper):
    def __init__(self):
        super(SpeakerTextJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        # Acquired by CloudFactory
        self.company.job_set.all().delete()

def get_scraper():
    return SpeakerTextJobScraper()
