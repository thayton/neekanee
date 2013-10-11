from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'Ketchum',
    'hq': 'New York, NY',

    'ats': 'icims',

    'home_page_url': 'http://www.ketchum.com',
    'jobs_page_url': 'https://careers-ketchum.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [1001,5000]
}

class KetchumJobScraper(IcimsJobScraper):
    def __init__(self):
        super(KetchumJobScraper, self).__init__(COMPANY)

def get_scraper():
    return KetchumJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
