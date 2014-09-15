import re, mechanize, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.urlutil import url_query_filter

from neekanee_solr.models import *

COMPANY = {
    'name': 'Acme Packet',
    'hq': 'Bedford, MA',

    'ats': 'silkroad',

    'home_page_url': 'http://www.acmepacket.com',
    'jobs_page_url': 'https://acmepacket.silkroad.com/epostings/index.cfm?&company_id=15878&version=1',

    'empcnt': [501,1000]
}

class AcmePacketJobScraper(JobScraper):
    def __init__(self):
        super(AcmePacketJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        # Acquired by Oracle
        self.company.job_set.all().delete()

def get_scraper():
    return AcmePacketJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
