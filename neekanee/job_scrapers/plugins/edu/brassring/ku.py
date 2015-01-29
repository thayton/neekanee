import re

from neekanee.jobscrapers.brassring.brassring import BrassringJobScraper
from neekanee.htmlparse.soupify import soupify

COMPANY = {
    'name': 'Universiy of Kansas',
    'hq': 'Lawrence, KS',

    'home_page_url': 'http://www.ku.edu',
    'jobs_page_url': 'https://sjobs.brassring.com/TGWebHost/home.aspx?partnerid=25752&siteid=5541',

    'empcnt': [10001]
}

class KuJobScraper(BrassringJobScraper):
    def __init__(self):
        super(KuJobScraper, self).__init__(COMPANY)
        self.soupify_search_form = True
        self.br.addheaders = [('User-agent', 
                               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7')]

    def get_title_from_formtext(self, x):
        s = soupify(x['JobTitle'])
        return s.a.text

    def get_location_from_formtext(self, x):
        l = self.parse_location(x['Location'])
        return l

    def get_url_from_formtext(self, x):
        s = soupify(x['JobTitle'])
        return s.a

def get_scraper():
    return KuJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
