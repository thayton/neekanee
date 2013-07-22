from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'MRY',
    'hq': 'New York NY',

    'home_page_url': 'http://mry.com',
    'jobs_page_url': 'http://mryouth.theresumator.com',

    'empcnt': [51,200]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
