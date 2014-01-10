from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'Bronto',
    'hq': 'Durham, NC',

    'home_page_url': 'http://bronto.com',
    'jobs_page_url': 'https://careers-bronto.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [51,200]
}

class BrontoJobScraper(IcimsJobScraper):
    def __init__(self):
        super(BrontoJobScraper, self).__init__(COMPANY)

def get_scraper():
    return BrontoJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
