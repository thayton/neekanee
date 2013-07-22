from neekanee.jobscrapers.jobscore.jobscore import JobScoreJobScraper

COMPANY = {
    'name': 'CloudFlare',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.cloudflare.com',
    'jobs_page_url': 'http://www.jobscore.com/jobs/cloudflare/',

    'empcnt': [11,50]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)
