from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Flavorpill',
    'hq': 'New York, NY',

    'home_page_url': 'http://www.flavorpill.com',
    'jobs_page_url': 'http://flavorpill.theresumator.com',

    'empcnt': [11,50]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
