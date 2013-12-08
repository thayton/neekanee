import re

from neekanee.jobscrapers.brassring.brassring import BrassringJobScraper
from neekanee.htmlparse.soupify import soupify

COMPANY = {
    'name': 'Exelis',
    'hq': 'McLean, VA',

    'home_page_url': 'http://www.exelisinc.com',
    'jobs_page_url': 'https://sjobs.brassring.com/1033/ASP/TG/cim_home.asp?partnerid=25326&siteid=5443',

    'empcnt': [10001]
}

class ExelisIncJobScraper(BrassringJobScraper):
    def __init__(self):
        super(ExelisIncJobScraper, self).__init__(COMPANY)
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
    return ExelisIncJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
