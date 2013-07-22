from neekanee.jobscrapers.jobscore.jobscore import JobScoreJobScraper

COMPANY = {
    'name': 'Sponge Cell',
    'hq': 'New York, NY',

    'home_page_url': 'http://www.spongecell.com',
    'jobs_page_url': 'http://spongecell.jobscore.com/list/',

    'empcnt': [11,50]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)
