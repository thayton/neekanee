from neekanee.jobscrapers.brassring.brassring import BrassringJobScraper
from neekanee.htmlparse.soupify import soupify

COMPANY = {
    'name': 'Westat',
    'hq': 'Rockville, MD',

    'home_page_url': 'http://www.westat.com',
    'jobs_page_url': 'https://sjobs.brassring.com/TGWebHost/home.aspx?partnerid=82&siteid=5197',

    'empcnt': [1001,5000]
}

class WestatJobScraper(BrassringJobScraper):
    def __init__(self):
        super(WestatJobScraper, self).__init__(COMPANY)
        self.soupify_search_form = True

    def get_url_from_formtext(self, x):
        s = soupify(x['AutoReq'])
        return s.a

    def get_title_from_formtext(self, x):
        return x['JobTitle']

    def get_location_from_formtext(self, x):
        l = x['Location']
        l = self.parse_location(l)

        return l

def get_scraper():
    return WestatJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
