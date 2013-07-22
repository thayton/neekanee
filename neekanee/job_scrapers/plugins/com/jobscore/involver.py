from neekanee.jobscrapers.jobscore.jobscore import JobScoreJobScraper

COMPANY = {
    'name': 'Involver',
    'hq': 'San Francisco, CA',

    'contact': 'jobs@involver.com',
    'benefits': {'vacation': [(1,20)]},

    'home_page_url': 'http://www.involver.com',
    'jobs_page_url': 'http://involver.jobscore.com/jobs/involver/list',

    'empcnt': [51,200]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)
