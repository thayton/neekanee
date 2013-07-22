import re

from neekanee.jobscrapers.brassring.brassring import BrassringJobScraper
from neekanee.htmlparse.soupify import soupify

COMPANY = {
    'name': 'Harvard University',
    'hq': 'Cambridge, MA',

    'ats': 'Kenexa',

    'home_page_url': 'http://www.harvard.edu',
    'jobs_page_url': 'https://sjobs.brassring.com/TGWebHost/home.aspx?partnerid=25240&siteid=5341',

    'empcnt': [10001]
}

class HarvardJobScraper(BrassringJobScraper):
    def __init__(self):
        super(HarvardJobScraper, self).__init__(COMPANY)
        self.soupify_search_form = True
        self.br.addheaders = [('User-agent', 
                               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7')]

    def get_title_from_formtext(self, x):
        y = {'onmouseover': True}
        s = soupify(x['FORMTEXT1'])
        a = s.find('a', attrs=y)
        return a.text

    def get_url_from_formtext(self, x):
        y = {'onmouseover': True}
        s = soupify(x['FORMTEXT1'])
        a = s.find('a', attrs=y)
        return a

    def get_location_from_desc(self, s):
        p = s.find('span', id='Location')
        return self.parse_location(p.text)

def get_scraper():
    return HarvardJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
