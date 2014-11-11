import re

from neekanee.jobscrapers.brassring.brassring import BrassringJobScraper
from neekanee.htmlparse.soupify import soupify

COMPANY = {
    'name': 'Washington Gas',
    'hq': 'Springfield, VA',

    'home_page_url': 'http://www.washgas.com',
    'jobs_page_url': 'https://sjobs.brassring.com/TGWebHost/home.aspx?partnerid=25998&siteid=5273',

    'empcnt': [1001,5000]
}

class GeJobScraper(BrassringJobScraper):
    def __init__(self):
        super(GeJobScraper, self).__init__(COMPANY)
        self.soupify_search_form = True

    def get_url_from_formtext(self, x):
        s = soupify(x['AutoReq'])
        return s.a

    def get_title_from_formtext(self, x):
        return x['JobTitle']

    def get_location_from_formtext(self, x):
        l = x['Location']
        l = self.parse_location(l)

        return l

def get_scraper():
    return GeJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
