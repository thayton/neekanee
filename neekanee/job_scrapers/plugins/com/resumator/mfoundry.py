from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'mFoundry',
    'hq': 'Larkspur, CA',

    'home_page_url': 'http://www.mfoundry.com',
    'jobs_page_url': 'http://mfoundry.theresumator.com',

    'empcnt': [51,200]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
