from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'The Pew Charitable Trusts',
    'hq': 'Philadelphia, PA',

    'ats': 'icims',

    'home_page_url': 'http://www.pewtrusts.org',
    'jobs_page_url': 'https://jobs-pct.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [501,1000]
}

class PewTrustsJobScraper(IcimsJobScraper):
    def __init__(self):
        super(PewTrustsJobScraper, self).__init__(COMPANY)

def get_scraper():
    return PewTrustsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
