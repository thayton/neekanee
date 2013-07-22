from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Digg',
    'hq': 'New York, NY',

    'home_page_url': 'http://www.digg.com',
    'jobs_page_url': 'http://digg.theresumator.com',

    'empcnt': [1,10]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
