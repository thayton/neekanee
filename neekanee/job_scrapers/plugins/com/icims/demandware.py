from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'Demandware',
    'hq': 'Burlington, MA',

    'home_page_url': 'http://www.demandware.com',
    'jobs_page_url': 'https://careers-demandware.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [201,500]
}

class DemandwareJobScraper(IcimsJobScraper):
    def __init__(self):
        super(DemandwareJobScraper, self).__init__(COMPANY)

def get_scraper():
    return DemandwareJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
