from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'Carbonite',
    'hq': 'Boston, MA',

    'ats': 'icims',

    'home_page_url': 'http://www.carbonite.com',
    'jobs_page_url': 'https://careers-carbonite.icims.com/jobs/intro?hashed=0&in_iframe=1',
    
    'empcnt': [51,200]
}

class CarboniteJobScraper(IcimsJobScraper):
    def __init__(self):
        super(CarboniteJobScraper, self).__init__(COMPANY)

def get_scraper():
    return CarboniteJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
