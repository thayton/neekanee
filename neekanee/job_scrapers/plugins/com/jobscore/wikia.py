from neekanee.jobscrapers.jobscore.jobscore import JobScoreJobScraper

COMPANY = {
    'name': 'Wikia',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.wikia.com',
    'jobs_page_url': 'http://www.jobscore.com/jobs/wikiainc/',

    'empcnt': [51,200]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
