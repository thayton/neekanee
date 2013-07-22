from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Cloudera',
    'hq': 'Palo Alto, CA',

    'home_page_url': 'http://www.cloudera.com',
    'jobs_page_url': 'http://cloudera.theresumator.com',

    'empcnt': [51,200]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
