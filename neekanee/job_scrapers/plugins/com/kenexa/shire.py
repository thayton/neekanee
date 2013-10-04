import re
from neekanee.jobscrapers.kenexa.kenexa import KenexaJobScraper

COMPANY = {
    'name': 'Shire',
    'hq': 'Dublin, Ireland',

    'ats': 'Kenexa',

    'home_page_url': 'http://www.shire.com',
    'jobs_page_url': 'https://sjobs.brassring.com/1033/ASP/TG/cim_home.asp?partnerid=25300&siteid=5445',

    'empcnt': [10001]
}

class ShireJobScraper(KenexaJobScraper):
    def __init__(self):
        super(ShireJobScraper, self).__init__(COMPANY)

    def follow_search_openings_link(self):
        self.br.follow_link(self.br.find_link(url_regex=re.compile(r'cim_advsearch\.asp')))

    def get_location_from_td(self, td):
        return self.parse_location(td[-3].text)
    
def get_scraper():
    return ShireJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
