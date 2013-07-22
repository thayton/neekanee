import re

from neekanee.jobscrapers.brassring.brassring import BrassringJobScraper
from neekanee.htmlparse.soupify import soupify

COMPANY = {
    'name': 'General Electric',
    'hq': 'Fairfield, CT',

    'home_page_url': 'http://www.ge.com',
    'jobs_page_url': 'https://xjobs.brassring.com/TGWebHost/home.aspx?partnerid=54&siteid=5346&codes=GECareers',

    'empcnt': [10001]
}

class GeJobScraper(BrassringJobScraper):
    def __init__(self):
        super(GeJobScraper, self).__init__(COMPANY)
        self.soupify_search_form = True

    def get_url_from_formtext(self, x):
        s = soupify(x['OptionalReq'])
        return s.a

    def get_title_from_formtext(self, x):
        return x['FORMTEXT26']

    def get_location_from_formtext(self, x):
        l = x['FORMTEXT11'] + ', ' + x['FORMTEXT22']
        l = self.parse_location(l)

        return l

def get_scraper():
    return GeJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
