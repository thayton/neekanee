from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Fat Wallet',
    'hq': 'Rockton, IL',

    'home_page_url': 'http://www.fatwallet.com',
    'jobs_page_url': 'http://fatwallet.theresumator.com',

    'empcnt': [51,200]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
