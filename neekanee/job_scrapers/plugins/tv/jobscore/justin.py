from neekanee.jobscrapers.jobscore.jobscore import JobScoreJobScraper

COMPANY = {
    'name': 'Jusin.tv',
    'hq': 'San Francisco, CA',

    'ats': 'JobVite',

    'home_page_url': 'http://www.justin.tv',
    'jobs_page_url': 'http://www.jobscore.com/jobs/twitch',

    'empcnt': [11,50]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)
