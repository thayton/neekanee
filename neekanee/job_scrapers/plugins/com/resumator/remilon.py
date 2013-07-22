from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Remilon',
    'hq': 'Mountain View, CA',

    'home_page_url': 'http://www.remilon.com',
    'jobs_page_url': 'http://remilon.theresumator.com',

    'empcnt': [11,50]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
