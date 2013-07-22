from neekanee.jobscrapers.jobscore.jobscore import JobScoreJobScraper

COMPANY = {
    'name': 'iSEC Partners',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.isecpartners.com',
    'jobs_page_url': 'http://www.jobscore.com/jobs/isecpartners/',

    'empcnt': [11,50]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)
