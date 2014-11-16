from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'Thales Defense and Security',
    'hq': 'Clarksburg, MD',

    'home_page_url': 'http://www.thalesdsi.com',
    'jobs_page_url': 'https://jobs-thalesdsi.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [51,200]
}

class ThalesJobScraper(IcimsJobScraper):
    def __init__(self):
        super(ThalesJobScraper, self).__init__(COMPANY)

def get_scraper():
    return ThalesJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
