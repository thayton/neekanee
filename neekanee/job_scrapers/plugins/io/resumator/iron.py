from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Iron.io',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.iron.io',
    'jobs_page_url': 'http://iron.theresumator.com',

    'empcnt': [11,50]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
