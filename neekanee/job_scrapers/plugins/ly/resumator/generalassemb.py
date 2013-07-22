import re, urlparse

from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'General Assemb.ly',
    'hq': 'New York, NY',

    'home_page_url': 'http://generalassemb.ly',
    'jobs_page_url': 'http://ga.theresumator.com/',

    'empcnt': [51,200]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
