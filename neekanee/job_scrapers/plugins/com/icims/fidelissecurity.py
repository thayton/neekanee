from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'Fidelis Security Systems',
    'hq': 'Bethesda, MD',

    'home_page_url': 'http://www.fidelissecurity.com',
    'jobs_page_url': 'https://careers-fidelissecuritysystems.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [11,50]
}

class FidelisSecurityJobScraper(IcimsJobScraper):
    def __init__(self):
        super(FidelisSecurityJobScraper, self).__init__(COMPANY)

def get_scraper():
    return FidelisSecurityJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
