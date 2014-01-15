from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'NCIRE',
    'hq': 'San Francisco, CA',

    'ats': 'icims',

    'home_page_url': 'http://www.ncire.org',
    'jobs_page_url': 'https://jobs-ncire.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [201,500]
}

class NcireJobScraper(IcimsJobScraper):
    def __init__(self):
        super(NcireJobScraper, self).__init__(COMPANY)
        self.use_company_location = True

def get_scraper():
    return NcireJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
