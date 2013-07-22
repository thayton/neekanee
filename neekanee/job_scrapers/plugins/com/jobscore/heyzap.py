from neekanee.jobscrapers.jobscore.jobscore import JobScoreJobScraper

COMPANY = {
    'name': 'Heyzap',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.heyzap.com',
    'jobs_page_url': 'http://heyzap.jobscore.com/jobs/heyzap/',

    'empcnt': [1,10]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)
