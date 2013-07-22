from neekanee.jobscrapers.jobscore.jobscore import JobScoreJobScraper

COMPANY = {
    'name': 'Xobni',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.xobni.com',
    'jobs_page_url': 'http://www.jobscore.com/jobs/xobni/',

    'empcnt': [11,50]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)
