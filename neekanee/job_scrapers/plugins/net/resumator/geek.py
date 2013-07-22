from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Geeknet',
    'hq': 'Fairfax, VA',

    'home_page_url': 'http://geek.net',
    'jobs_page_url': 'http://geek.theresumator.com',

    'empcnt': [51,200]
}

#
# Actually uses both Employease for some of the
# job listings and Resumator for other job listings
#
def get_scraper():
    return ResumatorJobScraper(COMPANY)
