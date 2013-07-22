from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Pawngo',
    'hq': 'Denver, CO',

    'home_page_url': 'http://www.pawngo.com',
    'jobs_page_url': 'http://pawngo.theresumator.com',

    'empcnt': [11,50]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
