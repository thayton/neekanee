import re

from neekanee.jobscrapers.brassring.brassring import BrassringJobScraper
from neekanee.htmlparse.soupify import soupify

COMPANY = {
    'name': 'Polaris Industries',
    'hq': 'Medina, MN',

    'home_page_url': 'http://www.polaris.com',
    'jobs_page_url': 'http://jobs.brassring.com/TGWebHost/home.aspx?partnerid=25672&siteid=5450',

    'empcnt': [5001,10000]
}

class PolarisJobScraper(BrassringJobScraper):
    def __init__(self):
        super(PolarisJobScraper, self).__init__(COMPANY)
        self.soupify_search_form = True

    def get_url_from_formtext(self, x):
        s = soupify(x['AutoReq'])
        return s.a

    def get_title_from_formtext(self, x):
        return x['JobTitle']

    def get_location_from_formtext(self, x):
        l = x['FORMTEXT17']
        l = self.parse_location(l)

        return l

def get_scraper():
    return PolarisJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
