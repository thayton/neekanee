from neekanee.jobscrapers.icims.icims import IcimsJobScraper

COMPANY = {
    'name': 'Fidelis Security Systems',
    'hq': 'Bethesda, MD',

    'home_page_url': 'http://www.fidelissecurity.com',
    'jobs_page_url': 'https://careers-fidelissecuritysystems.icims.com/jobs/intro',

    'empcnt': [11,50]
}

class FidelisSecurityJobScraper(IcimsJobScraper):
    def __init__(self):
        super(FidelisSecurityJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[2].text)

def get_scraper():
    return FidelisSecurityJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
