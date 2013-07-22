from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Next Big Sound',
    'hq': 'Boulder, CO',

    'home_page_url': 'http://www.nextbigsound.com',
    'jobs_page_url': 'http://nextbigsound.theresumator.com',

    'empcnt': [1,10]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
