from neekanee.jobscrapers.kenexa.kenexa import KenexaJobScraper

COMPANY = {
    'name': 'Westat',
    'hq': 'Rockville, MD',

    'home_page_url': 'http://www.westat.com',
    'jobs_page_url': 'https://sjobs.brassring.com/en/asp/tg/cim_home.asp?partnerid=82&siteid=5197',

    'empcnt': [1001,5000]
}

class WestatJobScraper(KenexaJobScraper):
    def __init__(self):
        super(WestatJobScraper, self).__init__(COMPANY)

    def get_title_from_td(self, td):
        return td[3].text

    def get_location_from_td(self, td):
        return self.parse_location(td[4].text)

def get_scraper():
    return WestatJobScraper()
