import re

from neekanee.jobscrapers.brassring.brassring import BrassringJobScraper
from neekanee.htmlparse.soupify import soupify

COMPANY = {
    'name': 'Novartis',
    'hq': 'Cambridge, MA',

    'home_page_url': 'http://www.novartis.com',
    'jobs_page_url': 'https://sjobs.brassring.com/tgwebhost/home.aspx?partnerid=13617&siteid=5260',

    'empcnt': [10001]
}

class NovartisJobScraper(BrassringJobScraper):
    def __init__(self):
        super(NovartisJobScraper, self).__init__(COMPANY)
        self.soupify_search_form = True

    def get_url_from_formtext(self, x):
        s = soupify(x['JobTitle'])
        return s.a

    def get_title_from_formtext(self, x):
        s = soupify(x['JobTitle'])
        return s.a.text

    def get_location_from_formtext(self, x):
        l = x['FORMTEXT28'] + ', ' + x['FORMTEXT27']
        l = self.parse_location(l)

        return l

def get_scraper():
    return NovartisJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
