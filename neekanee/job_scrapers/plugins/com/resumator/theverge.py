from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'The Verge',
    'hq': 'New York, NY',

    'home_page_url': 'http://www.theverge.com',
    'jobs_page_url': 'http://theverge.theresumator.com',

    'empcnt': [11,50]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
