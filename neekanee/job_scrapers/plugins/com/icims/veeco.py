from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'Veeco',
    'hq': 'Plainview, NY',

    'home_page_url': 'http://www.veeco.com',
    'jobs_page_url': 'https://hub-veeco.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [1001,5000]
}

class VeecoJobScraper(IcimsJobScraper):
    def __init__(self):
        super(VeecoJobScraper, self).__init__(COMPANY)

def get_scraper():
    return VeecoJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
