from neekanee.jobscrapers.jobscore.jobscore2 import JobScoreJobScraper

COMPANY = {
    'name': 'Ridejoy',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.ridejoy.com',
    'jobs_page_url': 'http://ridejoycom.jobscore.com/list',

    'empcnt': [11,50]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)
