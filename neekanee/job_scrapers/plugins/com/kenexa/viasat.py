from neekanee.jobscrapers.kenexa.kenexa import KenexaJobScraper

COMPANY = {
    'name': 'ViaSat',
    'hq': 'Carlsbad, CA',

    'ats': 'Kenexa',

    'home_page_url': 'http://www.viasat.com',
    'jobs_page_url': 'https://sjobs.brassring.com/1033/ASP/TG/cim_home.asp?partnerid=425&siteid=5199',

    'empcnt': [1001,5000]
}

class ViasatJobScraper(KenexaJobScraper):
    def __init__(self):
        super(ViasatJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[3].text)
    
def get_scraper():
    return ViasatJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
