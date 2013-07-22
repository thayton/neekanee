from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Cloudant',
    'hq': 'Boston, MA',

    'home_page_url': 'http://www.cloudant.com',
    'jobs_page_url': 'http://cloudant.theresumator.com',

    'empcnt': [11,50]
}
def get_scraper():
    return ResumatorJobScraper(COMPANY)
