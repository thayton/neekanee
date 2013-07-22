from neekanee.jobscrapers.brassring.brassring import BrassringJobScraper
from neekanee.htmlparse.soupify import soupify

COMPANY = {
    'name': 'Huntington Ingalls Industries',
    'hq': 'Newport News, VA',

    'home_page_url': 'http://www.huntingtoningalls.com',
    'jobs_page_url': 'https://sjobs.brassring.com/en/asp/tg/cim_home.asp?partnerid=25477&siteid=5548',

    'empcnt': [10001]
}

class HuntingtonIngallsJobScraper(BrassringJobScraper):
    def __init__(self):
        super(HuntingtonIngallsJobScraper, self).__init__(COMPANY)
        self.soupify_search_form = True

    def get_url_from_formtext(self, x):
        s = soupify(x['AutoReq'])
        return s.a

    def get_title_from_formtext(self, x):
        return x['FORMTEXT17']

    def get_location_from_formtext(self, x):
        return self.parse_location(x['FORMTEXT11'])

def get_scraper():
    return HuntingtonIngallsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
