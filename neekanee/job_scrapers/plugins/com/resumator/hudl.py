from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Hudl',
    'hq': 'Lincoln, NE',

    'home_page_url': 'http://www.hudl.com',
    'jobs_page_url': 'http://hudl.theresumator.com',

    'empcnt': [51,200]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
