from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Posterous',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.posterous.com',
    'jobs_page_url': 'http://posterous.theresumator.com',

    'empcnt': [1,10]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
