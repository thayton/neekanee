from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Metamarkets',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.metamarkets.com',
    'jobs_page_url': 'http://metamarkets.theresumator.com',

    'empcnt': [11,50]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
