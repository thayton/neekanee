from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'YCharts',
    'hq': 'New York, NY',

    'contact': 'jobs@ycharts.com',

    'home_page_url': 'http://ycharts.com',
    'jobs_page_url': 'http://ycharts.theresumator.com',

    'empcnt': [11,50]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
