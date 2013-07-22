from neekanee.jobscrapers.jobscore.jobscore import JobScoreJobScraper

COMPANY = {
    'name': 'Beer Bites LLC',
    'hq': 'Stratham, NH',

    'home_page_url': 'http://www.beerbites.com',
    'jobs_page_url': 'http://www.jobscore.com/jobs/beerbites/',

    'empcnt': [1,10]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)
