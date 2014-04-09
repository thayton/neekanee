from neekanee.jobscrapers.jobscore.jobscore2 import JobScoreJobScraper

COMPANY = {
    'name': 'CrowdFlower',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.crowdflower.com',
    'jobs_page_url': 'http://www.jobscore.com/jobs/crowdflower/',

    'empcnt': [11,50]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)
