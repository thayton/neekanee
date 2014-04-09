from neekanee.jobscrapers.jobscore.jobscore2 import JobScoreJobScraper

COMPANY = {
    'name': 'snowballfactory',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.snowballfactory.com',
    'jobs_page_url': 'http://awesm.jobscore.com/list',

    'empcnt': [1,10]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)
