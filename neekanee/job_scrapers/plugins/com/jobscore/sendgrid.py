from neekanee.jobscrapers.jobscore.jobscore2 import JobScoreJobScraper

COMPANY = {
    'name': 'SendGrid',
    'hq': 'Boulder, CO',

    'benefits': {'vacation': [(1,15)]},

    'home_page_url': 'http://sendgrid.com',
    'jobs_page_url': 'http://sendgrid.jobscore.com/list',

    'empcnt': [11,50]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)
