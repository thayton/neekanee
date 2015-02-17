import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, get_mailto

from neekanee_solr.models import *

COMPANY = {
    'name': 'Meraki',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://meraki.com',
    'jobs_page_url': 'https://meraki.cisco.com/jobs',

    'empcnt': [51,200]
}

class MerakiJobScraper(JobScraper):
    def __init__(self):
        super(MerakiJobScraper, self).__init__(COMPANY)
        self.br.addheaders = [('User-agent', 
                               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7')]

    def scrape_jobs(self):
        # Now owned by Cisco
        self.company.job_set.all().delete()

def get_scraper():
    return MerakiJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
