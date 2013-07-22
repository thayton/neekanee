from neekanee.jobscrapers.jobscore.jobscore import JobScoreJobScraper

COMPANY = {
    'name': 'Quid',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.quid.com',
    'jobs_page_url': 'http://quid.jobscore.com/list',

    'empcnt': [11,50]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)
