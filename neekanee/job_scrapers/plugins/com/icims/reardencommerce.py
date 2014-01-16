from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'Rearden Commerce',
    'hq': 'Foster City, CA',

    'home_page_url': 'http://www.reardencommerce.com/',
    'jobs_page_url': 'https://careers-reardencommerce.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [501,1000]
}

class ReardenCommerceJobScraper(IcimsJobScraper):
    def __init__(self):
        super(ReardenCommerceJobScraper, self).__init__(COMPANY)

def get_scraper():
    return ReardenCommerceJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
