import re

from neekanee.jobscrapers.kenexa.kenexa import KenexaJobScraper
from neekanee.htmlparse.soupify import soupify

COMPANY = {
    'name': 'EMC',
    'hq': 'Hopkinton, MA',

    'home_page_url': 'http://www.emc.com',
    'jobs_page_url': 'https://sjobs.brassring.com/1033/asp/tg/cim_home.asp?partnerid=20085&siteid=5109',

    'empcnt': [10001]
}

class EmcJobScraper(KenexaJobScraper):
    def __init__(self):
        super(EmcJobScraper, self).__init__(COMPANY)
        self.soupify_search_form = True

    def get_location_from_td(self, td):
        l = td[4].text
        l = l.split(',', 1)[0]

        return self.parse_location(l)

def get_scraper():
    return EmcJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
