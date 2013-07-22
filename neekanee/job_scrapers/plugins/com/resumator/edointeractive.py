from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'edo Interactive',
    'hq': 'Nashville, TN',

    'home_page_url': 'http://www.edointeractive.com',
    'jobs_page_url': 'http://edo.theresumator.com',

    'empcnt': [11,50]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
