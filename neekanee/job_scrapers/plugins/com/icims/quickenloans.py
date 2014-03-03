from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'Quicken Loans',
    'hq': 'Detroit, MI',

    'home_page_url': 'http://www.quickenloans.com',
    'jobs_page_url': 'https://careers-quickenloans.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [1001,5000]
}

class QuickenLoansJobScraper(IcimsJobScraper):
    def __init__(self):
        super(QuickenLoansJobScraper, self).__init__(COMPANY)

def get_scraper():
    return QuickenLoansJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
