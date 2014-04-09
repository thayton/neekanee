from neekanee.jobscrapers.jobscore.jobscore2 import JobScoreJobScraper

COMPANY = {
    'name': 'JobScore',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.jobscore.com',
    'jobs_page_url': 'http://www.jobscore.com/jobs/jobscore',

    'empcnt': [1,10]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)
