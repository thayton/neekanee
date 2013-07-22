from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'IGN Entertainment',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://corp.ign.com',
    'jobs_page_url': 'http://ign.theresumator.com',

    'empcnt': [201,500]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
