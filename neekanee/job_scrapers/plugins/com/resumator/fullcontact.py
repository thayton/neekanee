from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Full Contact',
    'hq': 'Denver, CO',

    'home_page_url': 'http://www.fullcontact.com',
    'jobs_page_url': 'http://fullcontact.theresumator.com',

    'empcnt': [11,50]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
