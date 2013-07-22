from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'GreenGoose',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.greengoose.com',
    'jobs_page_url': 'http://greengoose.theresumator.com',

    'empcnt': [1,10]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
