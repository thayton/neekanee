from neekanee.jobscrapers.cats.cats import CatsJobScraper

COMPANY = {
    'name': 'Immedia Semiconductor',
    'hq': 'Andover, MA',

    'home_page_url': 'http://www.immediasemi.com',
    'jobs_page_url': 'http://immedia.catsone.com/careers/',

    'empcnt': [11,50]
}

def get_scraper():
    return CatsJobScraper(COMPANY)
