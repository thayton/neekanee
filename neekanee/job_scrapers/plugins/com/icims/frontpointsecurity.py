from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'FrontPoint Security',
    'hq': 'McLean, VA',

    'ats': 'icims',

    'home_page_url': 'http://www.frontpointsecurity.com',
    'jobs_page_url': 'https://careers-frontpointsecurity.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [201,500]
}

class FrontPointSecurityJobScraper(IcimsJobScraper):
    def __init__(self):
        super(FrontPointSecurityJobScraper, self).__init__(COMPANY)

def get_scraper():
    return FrontPointSecurityJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
