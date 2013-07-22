from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'WHMCS',
    'hq': 'Milton Keynes, UK',

    'home_page_url': 'http://www.whmcs.com',
    'jobs_page_url': 'http://whmcs.theresumator.com',

    'empcnt': [11,50]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
