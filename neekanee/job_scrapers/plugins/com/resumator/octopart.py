from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Octopart',
    'hq': 'New York, NY',

    'contact': 'jobs@octopart.com',

    'home_page_url': 'http://octopart.com',
    'jobs_page_url': 'http://octopart.theresumator.com',

    'empcnt': [11,50]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
