from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'DeviantART',
    'hq': 'Hollywood, CA',

    'home_page_url': 'http://www.deviantart.com',
    'jobs_page_url': 'http://deviantart.theresumator.com',

    'empcnt': [5001,10000]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
