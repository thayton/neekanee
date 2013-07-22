from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Vera Institute of Justice',
    'hq': 'Brooklyn, NY',

    'home_page_url': 'http://www.vera.org',
    'jobs_page_url': 'http://vera.theresumator.com',

    'empcnt': [51,200]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
