import re

from neekanee.jobscrapers.kenexa.kenexa import KenexaJobScraper

COMPANY = {
    'name': 'Hughes',
    'hq': 'Germantown, MD',

    'ats': 'Kenexa',

    'benefits': {'vacation': [(1,15),(5,20)]},

    'home_page_url': 'http://www.hughes.com',
    'jobs_page_url': 'https://sjobs.brassring.com/EN/ASP/TG/cim_home.asp?PartnerId=514&SiteId=241&codes=',

    'empcnt': [1001,5000]
}

class HughesJobScraper(KenexaJobScraper):
    def __init__(self):
        super(HughesJobScraper, self).__init__(COMPANY)

    def get_location_from_desc(self, s):
        l = s.find('span', id=re.compile(r'Location'))
        return self.parse_location(l.text.strip())

def get_scraper():
    return HughesJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
