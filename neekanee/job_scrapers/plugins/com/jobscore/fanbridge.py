from neekanee.jobscrapers.jobscore.jobscore import JobScoreJobScraper

COMPANY = {
    'name': 'FanBridge',
    'hq': 'New York, NY',

    'home_page_url': 'http://www.fanbridge.com',
    'jobs_page_url': 'http://www.jobscore.com/jobs/fanbridge/',

    'empcnt': [11,50]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
