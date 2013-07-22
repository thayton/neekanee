from neekanee.jobscrapers.jobscore.jobscore import JobScoreJobScraper

COMPANY = {
    'name': 'Jaspersoft',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.jaspersoft.com',
    'jobs_page_url': 'http://jaspersoft.jobscore.com/list',

    'empcnt': [51,200]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)
