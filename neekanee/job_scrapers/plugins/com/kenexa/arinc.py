from neekanee.jobscrapers.kenexa.kenexa import KenexaJobScraper

COMPANY = {
    'name': 'Arinc',
    'hq': 'Annapolis, MD',

    'home_page_url': 'http://www.arinc.com',
    'jobs_page_url': 'https://sjobs.brassring.com/EN/ASP/TG/cim_home.asp?partnerid=10626&siteid=48',

    'empcnt': [1001,5000]
}

class ArincJobScraper(KenexaJobScraper):
    def __init__(self):
        super(ArincJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        l = ', '.join(['%s' % x.text for x in td[3:6]])
        return self.parse_location(l)
    
def get_scraper():
    return ArincJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
