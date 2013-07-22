from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Voxy',
    'hq': 'New York, NY',

    'home_page_url': 'http://www.voxy.com',
    'jobs_page_url': 'http://voxy.theresumator.com',

    'empcnt': [11,50]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
