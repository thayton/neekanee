from neekanee.jobscrapers.jobscore.jobscore import JobScoreJobScraper

COMPANY = {
    'name': 'BuzzFeed',
    'hq': 'New York, NY',

    'home_page_url': 'http://www.buzzfeed.com',
    'jobs_page_url': 'http://www.jobscore.com/jobs/buzzfeed/',

    'empcnt': [1,10]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)
