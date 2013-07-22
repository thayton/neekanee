from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Scoopler',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.scoopler.com',
    'jobs_page_url': 'http://scoopler.theresumator.com',

    'empcnt': [1,10]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
