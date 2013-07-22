from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Orbotix',
    'hq': 'Boulder, CO',

    'home_page_url': 'http://www.orbotix.com',
    'jobs_page_url': 'http://orbotix.theresumator.com/',

    'empcnt': [1,10]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
