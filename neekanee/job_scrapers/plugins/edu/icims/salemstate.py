from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'Salem State University',
    'hq': 'Salem, MA',

    'home_page_url': 'http://www.salemstate.edu',
    'jobs_page_url': 'https://careers-salemstate.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [1001,5000]
}

class SalemStateJobScraper(IcimsJobScraper):
    def __init__(self):
        super(SalemStateJobScraper, self).__init__(COMPANY)
        self.use_company_location = True

def get_scraper():
    return SalemStateJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
