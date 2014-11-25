import re

from neekanee.jobscrapers.brassring.brassring import BrassringJobScraper
from neekanee.htmlparse.soupify import soupify

COMPANY = {
    'name': 'ManTech',
    'hq': 'Fairfax, VA',

    'home_page_url': 'http://www.mantech.com',
    'jobs_page_url': 'http://jobs.brassring.com/TGWebHost/home.aspx?partnerid=10696&siteid=45',

    'empcnt': [5001,10000]
}

class ManTechJobScraper(BrassringJobScraper):
    def __init__(self):
        super(ManTechJobScraper, self).__init__(COMPANY)
        self.soupify_search_form = True

    def get_url_from_formtext(self, x):
        s = soupify(x['JobTitle'])
        return s.a

    def get_title_from_formtext(self, x):
        s = soupify(x['JobTitle'])
        a = s.findAll('a')
        return a[1].text

    def get_location_from_formtext(self, x):
        l = x['Location']
        l = self.parse_location(l)
        return l

def get_scraper():
    return ManTechJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
