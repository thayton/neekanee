from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'WePay',
    'hq': 'Palo Alto, CA',

    'home_page_url': 'http://www.wepay.com',
    'jobs_page_url': 'http://wepay.theresumator.com',

    'empcnt': [11,50]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
