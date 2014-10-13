from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'Agrium',
    'hq': 'Denver, CO',

    'home_page_url': 'http://www.agrium.com',
    'jobs_page_url': 'https://careers-agrium.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [10001]
}

class AgriumJobScraper(IcimsJobScraper):
    def __init__(self):
        super(AgriumJobScraper, self).__init__(COMPANY)

def get_scraper():
    return AgriumJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
