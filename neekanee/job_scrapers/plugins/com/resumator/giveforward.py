from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'GiveForward',
    'hq': 'Chicago, IL',

    'home_page_url': 'http://www.giveforward.com',
    'jobs_page_url': 'http://giveforward.theresumator.com',

    'empcnt': [1,10]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
