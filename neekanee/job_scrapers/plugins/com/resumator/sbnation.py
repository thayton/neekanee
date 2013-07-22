from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'SB Nation',
    'hq': 'Washington, DC',

    'home_page_url': 'http://www.sbnation.com',
    'jobs_page_url': 'http://sbnation.theresumator.com',

    'empcnt': [11,50]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
