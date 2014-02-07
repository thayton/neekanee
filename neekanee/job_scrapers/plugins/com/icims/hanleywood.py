from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'Hanley Wood',
    'hq': 'Washington, DC',

    'home_page_url': 'http://www.hanleywood.com',
    'jobs_page_url': 'https://careers-hanleywood.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [501, 1000]
}

class HanleyWoodJobScraper(IcimsJobScraper):
    def __init__(self):
        super(HanleyWoodJobScraper, self).__init__(COMPANY)

def get_scraper():
    return HanleyWoodJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
