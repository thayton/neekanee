import re

from neekanee.jobscrapers.brassring.brassring import BrassringJobScraper
from neekanee.htmlparse.soupify import soupify

COMPANY = {
    'name': 'Bright Horizons',
    'hq': 'Watertown, MA',

    'home_page_url': 'http://www.brighthorizons.com',
    'jobs_page_url': 'https://sjobs.brassring.com/TGWebHost/home.aspx?partnerid=25595&siteid=5216',

    'empcnt': [10001]
}

class BrightHorizonsJobScraper(BrassringJobScraper):
    def __init__(self):
        super(BrightHorizonsJobScraper, self).__init__(COMPANY)
        self.soupify_search_form = True

    def get_url_from_formtext(self, x):
        s = soupify(x['FORMTEXT13'])
        return s.a

    def get_title_from_formtext(self, x):
        s = soupify(x['FORMTEXT13'])
        return s.a.text

    def get_location_from_formtext(self, x):
        l = x['FORMTEXT12'] + ', ' + x['FORMTEXT8']
        l = self.parse_location(l)

        return l

def get_scraper():
    return BrightHorizonsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
