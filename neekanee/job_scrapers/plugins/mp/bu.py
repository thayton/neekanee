from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Bump Tecnologies',
    'hq': 'Mountain View, CA',

    'home_page_url': 'http://bu.mp',
    'jobs_page_url': 'http://bump.theresumator.com/',

    'empcnt': [11,50]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
