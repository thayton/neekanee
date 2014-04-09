from neekanee.jobscrapers.jobscore.jobscore2 import JobScoreJobScraper

COMPANY = {
    'name': 'Crunched',
    'hq': 'New York, NY',

    'home_page_url': 'http://www.crunced.com',
    'jobs_page_url': 'http://www.jobscore.com/jobs/Crunched/',

    'empcnt': [11,50]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)
