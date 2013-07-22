from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Linode',
    'hq': 'Galloway, NJ',

    'home_page_url': 'http://www.linode.com',
    'jobs_page_url': 'http://linode.theresumator.com',

    'empcnt': [11,50]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
