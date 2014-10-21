from neekanee.jobscrapers.brassring.brassring import BrassringJobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text, extract_form_fields

COMPANY = {
    'name': 'Shire',
    'hq': 'Dublin, Ireland',

    'home_page_url': 'http://www.shire.com',
    'jobs_page_url': 'https://sjobs.brassring.com/TGWebHost/home.aspx?partnerid=25300&siteid=5445',

    'empcnt': [10001]
}

class ShireJobScraper(BrassringJobScraper):
    def __init__(self):
        super(ShireJobScraper, self).__init__(COMPANY)
        self.soupify_search_form = True

    def get_url_from_formtext(self, x):
        s = soupify(x['FORMTEXT7'])
        a = s.findAll('a')
        return a[-1]

    def get_title_from_formtext(self, x):
        s = soupify(x['FORMTEXT7'])
        a = s.findAll('a')
        return a[-1].text

    def get_location_from_formtext(self, x):
        l = x['FORMTEXT11']
        l = self.parse_location(l)
        return l
    
def get_scraper():
    return ShireJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
