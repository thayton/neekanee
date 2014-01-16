from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'TE Connectivity',
    'hq': 'Berwyn, PA',

    'home_page_url': 'http://www.te.com',
    'jobs_page_url': 'https://jobs-tycoelectronics.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [10001]
}

class TeJobScraper(IcimsJobScraper):
    def __init__(self):
        super(TeJobScraper, self).__init__(COMPANY)

def get_scraper():
    return TeJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
