import re
from neekanee.jobscrapers.kenexa.kenexa import KenexaJobScraper

COMPANY = {
    'name': 'Alcoa',
    'hq': 'Pittsburgh, PA',

    'ats': 'Kenexa',

    'home_page_url': 'http://www.alcoa.com',
    'jobs_page_url': 'https://sjobs.brassring.com/EN/ASP/TG/cim_home.asp?partnerid=16&siteid=56',

    'empcnt': [10001]
}

class AlcoaJobScraper(KenexaJobScraper):
    def __init__(self):
        super(AlcoaJobScraper, self).__init__(COMPANY)

    def follow_search_openings_link(self):
        self.br.follow_link(self.br.find_link(url_regex=re.compile(r'cim_advsearch\.asp')))

    def get_location_from_td(self, td):
        return self.parse_location(td[-3].text)
    
def get_scraper():
    return AlcoaJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
