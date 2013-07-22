from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'VaynerMedia',
    'hq': 'New York, NY',

    'home_page_url': 'http://www.vaynermedia.com',
    'jobs_page_url': 'http://vaynermedia.theresumator.com',

    'empcnt': [11,50]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
