from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'TextLinkBrokers',
    'hq': 'Mesa, AZ',

    'home_page_url': 'http://www.textlinkbrokers.com',
    'jobs_page_url': 'http://textlinkbrokers.theresumator.com',

    'empcnt': [51,200]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
