from neekanee.jobscrapers.jobscore.jobscore2 import JobScoreJobScraper

COMPANY = {
    'name': 'Performable',
    'hq': 'Cambridge, MA',

    'home_page_url': 'http://www.performable.com',
    'jobs_page_url': 'http://performable.jobscore.com/jobs/performable/list',

    'empcnt': [11,50]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)
