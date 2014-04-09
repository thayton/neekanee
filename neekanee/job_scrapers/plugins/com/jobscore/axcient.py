from neekanee.jobscrapers.jobscore.jobscore2 import JobScoreJobScraper

COMPANY = {
    'name': 'Axcient',
    'hq': 'Mountain View, CA',

    'home_page_url': 'http://www.axcient.com',
    'jobs_page_url': 'http://www.jobscore.com/jobs/axcientinc/',

    'empcnt': [11,50]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)
