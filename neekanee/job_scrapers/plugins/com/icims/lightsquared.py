from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'LightSquared',
    'hq': 'Reston, VA',

    'home_page_url': 'http://www.lightsquared.com',
    'jobs_page_url': 'https://jobs-lightsquared.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [201,500]
}

class LightSquaredJobScraper(IcimsJobScraper):
    def __init__(self):
        super(LightSquaredJobScraper, self).__init__(COMPANY)

def get_scraper():
    return LightSquaredJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
