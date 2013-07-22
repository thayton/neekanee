from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'TrackAbout',
    'hq': 'Moon Township, PA',

    'home_page_url': 'http://www.trackabout.com',
    'jobs_page_url': 'http://trackabout.theresumator.com',

    'empcnt': [11,50]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)
