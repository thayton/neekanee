from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Storenvy',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.storenvy.com',
    'jobs_page_url': 'http://storenvy.theresumator.com/apply',

    'empcnt': [1,10]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
