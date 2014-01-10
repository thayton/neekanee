from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'Fishnet Security',
    'hq': 'Overland Park, KS',

    'ats': 'icims',

    'home_page_url': 'http://www.fishnetsecurity.com',
    'jobs_page_url': 'https://careers-fishnetsecurity.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [201,500]
}

class FishnetJobScraper(IcimsJobScraper):
    def __init__(self):
        super(FishnetJobScraper, self).__init__(COMPANY)

def get_scraper():
    return FishnetJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
