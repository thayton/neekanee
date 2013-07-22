from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Mahalo',
    'hq': 'Culver City, CA',

    'home_page_url': 'http://www.mahalo.com',
    'jobs_page_url': 'http://mahalo.theresumator.com',

    'empcnt': [51,200]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
