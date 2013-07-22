from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Scoutmob',
    'hq': 'Atlanta, GA',

    'home_page_url': 'http://www.scoutmob.com',
    'jobs_page_url': 'http://scoutmob.theresumator.com',

    'empcnt': [51,200]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
