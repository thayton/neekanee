import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'ScanScout',
    'hq': 'Boston, MA',

    'home_page_url': 'http://www.scanscout.com',
    'jobs_page_url': 'http://www.scanscout.com/about_careers.php#careers-00006',

    'empcnt': [11,50]
}

class ScanScoutJobScraper(JobScraper):
    def __init__(self):
        super(ScanScoutJobScraper, self).__init__(COMPANY)

    def scrape_jobs(self):
        # Acquired by Tremor Media
        # http://paidcontent.org/2010/11/08/419-online-video-ad-net-tremor-media-acquires-scanscout/
        self.company.job_set.all().delete()

def get_scraper():
    return ScanScoutJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
