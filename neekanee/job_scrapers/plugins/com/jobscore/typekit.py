from neekanee.jobscrapers.jobscore.jobscore2 import JobScoreJobScraper

COMPANY = {
    'name': 'Typekit',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.typekit.com',
    'jobs_page_url': 'http://typekit.jobscore.com/list',

    'empcnt': [11,50]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)
