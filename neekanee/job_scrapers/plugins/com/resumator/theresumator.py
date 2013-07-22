from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'The Resumator',
    'hq': 'Pittsburgh, PA',

    'home_page_url': 'http://www.theresumator.com',
    'jobs_page_url': 'http://jobs.theresumator.com',

    'empcnt': [1,10]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
