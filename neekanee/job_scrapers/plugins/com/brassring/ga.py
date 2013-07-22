import re

from neekanee.jobscrapers.brassring.brassring import BrassringJobScraper
from neekanee.htmlparse.soupify import soupify

COMPANY = {
    'name': 'General Atomics',
    'hq': 'San Diego, CA',

    'home_page_url': 'http://www.ga.com',
    'jobs_page_url': 'https://sjobs.brassring.com/TGWebHost/home.aspx?PartnerId=25539&SiteId=5313&codes=IIND',

    'empcnt': [5001, 10000]
}

class GaJobScraper(BrassringJobScraper):
    def __init__(self):
        super(GaJobScraper, self).__init__(COMPANY)
        self.soupify_search_form = True

    def get_url_from_formtext(self, x):
        s = soupify(x['AutoReq'])
        return s.a

    def get_title_from_formtext(self, x):
        return x['FORMTEXT8']

    def get_location_from_formtext(self, x):
        l = x['FORMTEXT5'] + ', ' + x['FORMTEXT4']
        l = self.parse_location(l)

        return l

def gat_scraper():
    return GaJobScraper()

if __name__ == '__main__':
    job_scraper = gat_scraper()
    job_scraper.scrape_jobs()
