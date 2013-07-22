import re, urlparse

from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'bit.ly',
    'hq': 'New York, NY',

    'contact': 'jobs@bit.ly',

    'home_page_url': 'http://bit.ly',
    'jobs_page_url': 'http://bitly.theresumator.com/',

    'empcnt': [11,50]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
