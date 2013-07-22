from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Local Orbit',
    'hq': 'Ann Arbor, MI',

    'home_page_url': 'http://localorb.it',
    'jobs_page_url': 'http://localorbit.theresumator.com',

    'empcnt': [1,10]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
