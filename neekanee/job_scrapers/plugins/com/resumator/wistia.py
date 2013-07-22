from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Wistia',
    'hq': 'Somerville, MA',

    'home_page_url': 'http://www.wistia.com',
    'jobs_page_url': 'http://wistia.theresumator.com',

    'empcnt': [1,10]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
