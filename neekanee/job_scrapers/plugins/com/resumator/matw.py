from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Matthews International',
    'hq': 'Pittsburgh, PA',

    'home_page_url': 'http://www.matw.com',
    'jobs_page_url': 'http://matthews.theresumator.com',

    'empcnt': [1001,5000]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
