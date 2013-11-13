from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'Watchfire Signs',
    'hq': 'Danville, IL',

    'home_page_url': 'http://www.watchfiresigns.com',
    'jobs_page_url': 'https://jobs-watchfiresigns.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [201,500]
}

class WatchFireJobScraper(IcimsJobScraper):
    def __init__(self):
        super(WatchFireJobScraper, self).__init__(COMPANY)

def get_scraper():
    return WatchFireJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
