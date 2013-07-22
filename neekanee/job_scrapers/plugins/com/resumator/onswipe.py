from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'OnSwipe',
    'hq': 'New York, NY',

    'home_page_url': 'http://www.onswipe.com',
    'jobs_page_url': 'http://onswipe.theresumator.com/apply',

    'empcnt': [1,10]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
