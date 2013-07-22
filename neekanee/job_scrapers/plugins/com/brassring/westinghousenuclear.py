from neekanee.jobscrapers.brassring.brassring import BrassringJobScraper
from neekanee.htmlparse.soupify import soupify

COMPANY = {
    'name': 'Westinghouse',
    'hq': 'Cranberry Township, PA',

    'home_page_url': 'http://www.westinghousenuclear.com',
    'jobs_page_url': 'https://sjobs.brassring.com/TGWebHost/home.aspx?partnerid=11716&siteid=113',

    'empcnt': [10001]
}

class WestinghouseNuclearJobScraper(BrassringJobScraper):
    def __init__(self):
        super(WestinghouseNuclearJobScraper, self).__init__(COMPANY)
        self.soupify_search_form = True

    def get_url_from_formtext(self, x):
        s = soupify(x['FORMTEXT20'])
        return s.a

    def get_title_from_formtext(self, x):
        s = soupify(x['FORMTEXT20'])
        return s.a.text

    def get_location_from_formtext(self, x):
        l = x['FormText1']
        l = self.parse_location(l)

        return l

def get_scraper():
    return WestinghouseNuclearJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
