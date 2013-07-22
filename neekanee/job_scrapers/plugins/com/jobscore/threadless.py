from neekanee.jobscrapers.jobscore.jobscore import JobScoreJobScraper

COMPANY = {
    'name': 'Threadless',
    'hq': 'Chicago, IL',

    'home_page_url': 'http://www.threadless.com',
    'jobs_page_url': 'http://threadless.jobscore.com/list',

    'empcnt': [1,10]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)
