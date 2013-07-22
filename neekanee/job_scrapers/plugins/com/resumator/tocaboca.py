from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Tocaboca',
    'hq': 'Stockholm, Sweden',

    'home_page_url': 'http://tocaboca.com',
    'jobs_page_url': 'http://tocaboca.theresumator.com',

    'empcnt': [11,50]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
