from neekanee.jobscrapers.jobscore.jobscore2 import JobScoreJobScraper

COMPANY = {
    'name': 'Twilio',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.twilio.com',
    'jobs_page_url': 'http://twilio.jobscore.com/list',

    'empcnt': [11,50]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)
