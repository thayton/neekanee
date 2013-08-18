from neekanee.jobscrapers.brassring.brassring import BrassringJobScraper
from neekanee.htmlparse.soupify import soupify

from neekanee.jobscrapers.brassring.brassring import BrassringJobScraper

COMPANY = {
    'name': 'Duke University',
    'hq': 'Durham, NC',

    'home_page_url': 'http://www.duke.edu',
    'jobs_page_url': 'https://sjobs.brassring.com/TGWebHost/home.aspx?partnerid=25017&siteid=5172',

    'empcnt': [10001]
}

class DukeJobScraper(BrassringJobScraper):
    def __init__(self):
        super(DukeJobScraper, self).__init__(COMPANY)

        self.soupify_search_form = True

    def get_url_from_formtext(self, x):
        s = soupify(x['JobTitle'])
        return s.a

    def get_title_from_formtext(self, x):
        s = soupify(x['JobTitle'])
        return s.a.text

    def get_location_from_formtext(self, x):
        l = x['Location']
        l = self.parse_location(l)

        return l

def get_scraper():
    return DukeJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
