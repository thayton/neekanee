from neekanee.jobscrapers.kenexa.kenexa import KenexaJobScraper

COMPANY = {
    'name': 'BP Global',
    'hq': 'London, England',

    'ats': 'Kenexa',

    'home_page_url': 'http://www.bp.com',
    'jobs_page_url': 'https://careers.bpglobal.com/2057/ASP/TG/cim_home.asp?PartnerId=25078&SiteId=5012',

    'empcnt': [10001]
}

class BpJobScraper(KenexaJobScraper):
    def __init__(self):
        super(BpJobScraper, self).__init__(COMPANY)
        self.soupify_search_form = True

    def get_location_from_desc(self, s):
        reg = s.find('span', id='Countries (State/Region)')
        loc = s.find('span', id='Location')
        l = self.parse_location(loc.text + ', ' + reg.text)

        return l
    
def get_scraper():
    return BpJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
