from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Zumper',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.zumper.com',
    'jobs_page_url': 'http://zumper.theresumator.com',

    'empcnt': [1,10]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
