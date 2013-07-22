from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Wingu',
    'hq': 'Cambridge, MA',

    'home_page_url': 'http://www.wingu.com',
    'jobs_page_url': 'http://wingu.theresumator.com',

    'empcnt': [11,50]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
