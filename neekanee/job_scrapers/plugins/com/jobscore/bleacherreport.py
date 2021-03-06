from neekanee.jobscrapers.jobscore.jobscore2 import JobScoreJobScraper

COMPANY = {
    'name': 'Bleacher Report',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://bleacherreport.com',
    'jobs_page_url': 'http://www.jobscore.com/jobs/bleacherreport/',

    'empcnt': [11,50]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)
