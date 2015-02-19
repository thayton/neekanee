import re, urlparse

from neekanee.jobscrapers.jobscraper import JobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text
from neekanee.txtextract.pdftohtml import pdftohtml

from neekanee_solr.models import *

COMPANY = {
    'name': 'Institute for Transportation & Development Policy',
    'hq': 'New York, NY',

    'home_page_url': 'http://www.itdp.org',
    'jobs_page_url': 'https://www.itdp.org/who-we-are/jobs/',

    'empcnt': [11,50]
}

class ItdpJobScraper(JobScraper):
    def __init__(self):
        super(ItdpJobScraper, self).__init__(COMPANY)
        self.br.addheaders = [('User-agent', 
                               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7')]

    def scrape_jobs(self):
        # HTML is too unstructured
        self.company.job_set.all().delete()

def get_scraper():
    return ItdpJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
