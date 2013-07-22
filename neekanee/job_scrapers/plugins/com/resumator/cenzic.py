from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Cenzic',
    'hq': 'Campbell, CA',

    'home_page_url': 'http://www.cenzic.com',
    'jobs_page_url': 'http://cenzic.theresumator.com',

    'empcnt': [51,200]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
