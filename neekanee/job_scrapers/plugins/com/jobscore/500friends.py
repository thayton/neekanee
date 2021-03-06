from neekanee.jobscrapers.jobscore.jobscore2 import JobScoreJobScraper

COMPANY = {
    'name': '500friends',
    'hq': 'Berkeley, CA',

    'home_page_url': 'http://www.500friends.com',
    'jobs_page_url': 'http://www.jobscore.com/jobs/500friendsinc/',

    'empcnt': [11,50]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
