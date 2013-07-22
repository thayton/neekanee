from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'DuoLingo',
    'hq': 'Pittsburgh, PA',

    'home_page_url': 'http://www.duolingo.com',
    'jobs_page_url': 'http://duolingo.theresumator.com',

    'empcnt': [1,10]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
