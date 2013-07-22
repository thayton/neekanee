from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Deeplocal',
    'hq': 'Pittsburgh, PA',

    'home_page_url': 'http://www.deeplocal.com',
    'jobs_page_url': 'http://deeplocal.theresumator.com',

    'empcnt': [11,50]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
