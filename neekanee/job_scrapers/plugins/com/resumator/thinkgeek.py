from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'ThinkGeek',
    'hq': 'Fairfax, VA',

    'home_page_url': 'http://www.thinkgeek.com',
    'jobs_page_url': 'http://thinkgeek.theresumator.com',

    'empcnt': [11,50]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
