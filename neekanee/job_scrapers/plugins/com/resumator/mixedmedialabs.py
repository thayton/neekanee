from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Mixed Media Labs',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://mixedmedialabs.com',
    'jobs_page_url': 'http://picplz.theresumator.com/apply',

    'empcnt': [1,10]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)

