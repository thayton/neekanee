from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'ReverbNation',
    'hq': 'Durham, NC',

    'home_page_url': 'http://www.reverbnation.com',
    'jobs_page_url': 'http://reverbnation.theresumator.com',

    'empcnt': [51,200]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
