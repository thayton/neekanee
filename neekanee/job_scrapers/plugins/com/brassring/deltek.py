import re

from neekanee.jobscrapers.brassring.brassring import BrassringJobScraper
from neekanee.htmlparse.soupify import soupify

COMPANY = {
    'name': 'Deltek',
    'hq': 'Herndon, VA',

    'home_page_url': 'http://www.deltek.com',
    'jobs_page_url': 'https://sjobs.brassring.com/TGWebHost/home.aspx?partnerid=25397&siteid=5259',

    'empcnt': [1001,5000]
}

class DeltekJobScraper(BrassringJobScraper):
    def __init__(self):
        super(DeltekJobScraper, self).__init__(COMPANY)
        self.soupify_search_form = True

    def get_url_from_formtext(self, x):
        s = soupify(x['FORMTEXT4'])
        return s.a

    def get_title_from_formtext(self, x):
        s = soupify(x['FORMTEXT4'])
        return s.a.text

    def get_location_from_formtext(self, x):
        l = x['FORMTEXT1']
        l = self.parse_location(l)

        return l

def get_scraper():
    return DeltekJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
