from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Weebly',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.weebly.com',
    'jobs_page_url': 'http://weebly.theresumator.com',

    'empcnt': [11,50]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
