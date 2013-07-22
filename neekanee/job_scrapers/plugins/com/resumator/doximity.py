from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Doximity',
    'hq': 'San Mateo, CA',

    'home_page_url': 'http://www.doximity.com',
    'jobs_page_url': 'http://doximity.theresumator.com',

    'empcnt': [11,50]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
