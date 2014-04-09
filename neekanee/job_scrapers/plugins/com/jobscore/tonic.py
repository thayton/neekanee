from neekanee.jobscrapers.jobscore.jobscore2 import JobScoreJobScraper

COMPANY = {
    'name': 'Tonic',
    'hq': 'San Mateo, CA',

    'home_page_url': 'http://www.tonic.com',
    'jobs_page_url': 'http://tonic.jobscore.com/list',

    'empcnt': [11,50]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)
