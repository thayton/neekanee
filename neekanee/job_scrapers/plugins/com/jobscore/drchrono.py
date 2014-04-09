from neekanee.jobscrapers.jobscore.jobscore2 import JobScoreJobScraper

COMPANY = {
    'name': 'DrChrono',
    'hq': 'Mountain View, CA',

    'home_page_url': 'https://drchrono.com',
    'jobs_page_url': 'https://www.jobscore.com/jobs/drchrono/',

    'empcnt': [11,50]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)
