from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Catch',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.catch.com',
    'jobs_page_url': 'http://catch.theresumator.com',

    'empcnt': [11,50]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
