from neekanee.jobscrapers.kenexa.kenexa import KenexaJobScraper

COMPANY = {
    'name': 'Bose',
    'hq': 'Framingham, MA',

    'ats': 'Kenexa',

    'home_page_url': 'http://www.bose.com',
    'jobs_page_url': 'https://sjobs.brassring.com/EN/ASP/TG/cim_home.asp?partnerid=3&siteid=58',

    'empcnt': [5001,10000]
}

class BoseJobScraper(KenexaJobScraper):
    def __init__(self):
        super(BoseJobScraper, self).__init__(COMPANY)

    def get_title_from_td(self, td):
        return td[3].text

    def get_location_from_td(self, td):
        y = td[4].text + ',' + td[5].text
        return self.parse_location(y)

def get_scraper():
    return BoseJobScraper()
