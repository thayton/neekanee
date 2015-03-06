import re, urlparse
from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

from neekanee_solr.models import *

COMPANY = {
    'name': 'Mandiant',
    'hq': 'Alexandria, VA',

    'home_page_url': 'https://www.mandiant.com',
    'jobs_page_url': 'https://www.mandiant.com/company/careers/',

    'empcnt': [11,50]
}

class MandiantJobScraper(JobScraper):
    def __init__(self):
        super(MandiantJobScraper, self).__init__(COMPANY)
        self.br.addheaders = [('User-agent', 
                               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7')]

    def scrape_jobs(self):
        # Acquired
        self.company.job_set.all().delete()

def get_scraper():
    return MandiantJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
