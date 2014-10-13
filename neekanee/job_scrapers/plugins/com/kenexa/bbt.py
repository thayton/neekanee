from neekanee.jobscrapers.brassring.brassring import BrassringJobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, extract_form_fields

COMPANY = {
    'name': 'BB&T',
    'hq': 'Winston-Salem, NC',

    'ats': 'Kenexa',

    'home_page_url': 'http://www.bbt.com',
    'jobs_page_url': 'https://sjobs.brassring.com/TGWebHost/home.aspx?partnerid=25999&siteid=5373',

    'empcnt': [10001]
}

class BbtJobScraper(BrassringJobScraper):
    def __init__(self):
        super(BbtJobScraper, self).__init__(COMPANY)
        self.soupify_search_form = True

    def get_url_from_formtext(self, x):
        s = soupify(x['AutoReq'])
        return s.a

    def get_title_from_formtext(self, x):
        return x['JobTitle']

    def get_location_from_formtext(self, x):
        l = x['Location'].split('-')[0]
        l = self.parse_location(l)
        return l
            
def get_scraper():
    return BbtJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
