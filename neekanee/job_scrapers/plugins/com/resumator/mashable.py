from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Mashable',
    'hq': 'New York, NY',

    'home_page_url': 'http://mashable.com',
    'jobs_page_url': 'http://mashable.theresumator.com',

    'empcnt': [51,200]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
