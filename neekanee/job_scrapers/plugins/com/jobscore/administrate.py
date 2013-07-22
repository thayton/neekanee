from neekanee.jobscrapers.jobscore.jobscore import JobScoreJobScraper

COMPANY = {
    'name': 'Administrate',
    'hq': 'Glasgow, Scotland, United Kingdom',

    'home_page_url': 'http://www.administrate.com',
    'jobs_page_url': 'http://www.jobscore.com/jobs/administrate/',

    'empcnt': [11,50]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)
