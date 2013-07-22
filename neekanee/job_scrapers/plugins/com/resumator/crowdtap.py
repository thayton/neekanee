from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Crowdtap',
    'hq': 'New York, NY',

    'home_page_url': 'http://crowdtap.it',
    'jobs_page_url': 'http://crowdtap.theresumator.com',

    'empcnt': [51,200]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
