from neekanee.jobscrapers.jobscore.jobscore2 import JobScoreJobScraper

COMPANY = {
    'name': 'IAC',
    'hq': 'New York, NY',

    'home_page_url': 'http://www.iac.com',
    'jobs_page_url': 'http://www.jobscore.com/jobs2/iac',

    'empcnt': [1001,5000]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
