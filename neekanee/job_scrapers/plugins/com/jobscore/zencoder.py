from neekanee.jobscrapers.jobscore.jobscore2 import JobScoreJobScraper

COMPANY = {
    'name': 'Zencoder',
    'hq': 'Minneapolis, MN',

    'home_page_url': 'http://www.zencoder.com',
    'jobs_page_url': 'http://zencoder.jobscore.com/jobs/zencoder/list/',

    'empcnt': [11,50]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)
