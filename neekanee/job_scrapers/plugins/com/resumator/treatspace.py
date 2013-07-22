from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Treatspace',
    'hq': 'Pittsburgh, PA',

    'home_page_url': 'http://www.treatspace.com',
    'jobs_page_url': 'http://treatspace.theresumator.com',

    'empcnt': [5001,10000]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
