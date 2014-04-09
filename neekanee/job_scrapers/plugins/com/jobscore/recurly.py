from neekanee.jobscrapers.jobscore.jobscore2 import JobScoreJobScraper

COMPANY = {
    'name': 'Recurly',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://recurly.com',
    'jobs_page_url': 'http://recurly.jobscore.com/list',

    'empcnt': [1,10]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)
