from neekanee.jobscrapers.brassring.brassring import BrassringJobScraper
from neekanee.htmlparse.soupify import soupify

from neekanee_solr.models import *

COMPANY = {
    'name': 'BBN',
    'hq': 'Cambridge, MA',

    'ats': 'Kenexa',

    'home_page_url': 'http://www.bbn.com',
    'jobs_page_url': 'http://careers.bbn.com/TGWebHost/home.aspx?partnerid=25938&siteid=5179',

    'empcnt': [501, 1000]
}

class BbnJobScraper(BrassringJobScraper):
    def __init__(self):
        super(BbnJobScraper, self).__init__(COMPANY)
        self.soupify_search_form = True
            
    def get_url_from_formtext(self, x):
        s = soupify(x['JobTitle'])
        return s.a

    def get_title_from_formtext(self, x):
        s = soupify(x['JobTitle'])
        a = s.findAll('a')
        return a[-1].text

    def get_location_from_formtext(self, x):
        l = self.parse_location(x['FORMTEXT3'])
        return l

def get_scraper():
    return BbnJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
