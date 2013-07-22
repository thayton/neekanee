from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'CarWoo',
    'hq': 'Burlingame, CA',

    'home_page_url': 'http://www.carwoo.com',
    'jobs_page_url': 'http://carwoo.theresumator.com',

    'empcnt': [5001,10000]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
