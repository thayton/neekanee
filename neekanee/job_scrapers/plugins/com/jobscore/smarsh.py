from neekanee.jobscrapers.jobscore.jobscore import JobScoreJobScraper

COMPANY = {
    'name': 'Smarsh',
    'hq': 'Portland, OR',

    'home_page_url': 'http://www.smarsh.com',
    'jobs_page_url': 'http://www.jobscore.com/jobs/smarsh/list',

    'empcnt': [51,200]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)
