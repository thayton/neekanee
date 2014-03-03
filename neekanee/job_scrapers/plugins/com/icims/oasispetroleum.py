from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'Oasis Petroleum',
    'hq': 'Houston, TX',

    'home_page_url': 'http://www.oasispetroleum.com',
    'jobs_page_url': 'https://jobs-oasispetroleum.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [201,500]
}

class OasisPetroleumJobScraper(IcimsJobScraper):
    def __init__(self):
        super(OasisPetroleumJobScraper, self).__init__(COMPANY)

def get_scraper():
    return OasisPetroleumJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
