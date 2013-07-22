from neekanee.jobscrapers.jobscore.jobscore2 import JobScoreJobScraper

COMPANY = {
    'name': 'PagerDuty',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.pagerduty.com',
    'jobs_page_url': 'http://www.jobscore.com/jobs2/pagerduty',

    'empcnt': [1,10]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
