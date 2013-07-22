from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Fashiolista',
    'hq': 'Amsterdam, Netherlands',

    'home_page_url': 'http://www.fashiolista.com',
    'jobs_page_url': 'http://fashiolista.theresumator.com',

    'empcnt': [11,50]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
