import re

from neekanee.jobscrapers.brassring.brassring import BrassringJobScraper
from neekanee.htmlparse.soupify import soupify

COMPANY = {
    'name': 'Teradyne',
    'hq': 'North Reading, MA',

    'home_page_url': 'http://www.teradyne.com',
    'jobs_page_url': 'https://sjobs.brassring.com/TGWebHost/home.aspx?partnerid=20076&siteid=5048',

    'empcnt': [1001,5000]
}

class TeradyneJobScraper(BrassringJobScraper):
    def __init__(self):
        super(TeradyneJobScraper, self).__init__(COMPANY)
        self.soupify_search_form = True

    def get_url_from_formtext(self, x):
        s = soupify(x['FORMTEXT3'])
        return s.a

    def get_title_from_formtext(self, x):
        a = soupify(x['FORMTEXT3']).a
        return a.text

    def get_location_from_formtext(self, x):
        l = re.sub('HR-\S+', '', x['FORMTEXT1'])
        l = self.parse_location(l)

        return l

def get_scraper():
    return TeradyneJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
