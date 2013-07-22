from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Kembrel',
    'hq': 'Philadelphia, PA',

    'home_page_url': 'http://www.kembrel.com',
    'jobs_page_url': 'http://kembrel.theresumator.com',

    'empcnt': [1,10]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
