from neekanee.jobscrapers.jobscore.jobscore import JobScoreJobScraper

COMPANY = {
    'name': 'LearnBoost',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.learnboost.com',
    'jobs_page_url': 'http://www.jobscore.com/jobs/learnboost/',

    'empcnt': [1,10]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)
