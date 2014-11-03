from neekanee.jobscrapers.jobscore.jobscore2 import JobScoreJobScraper

COMPANY = {
    'name': 'Orchestrate',
    'hq': 'Portland, OR',

    'home_page_url': 'http://www.orchestrate.com',
    'jobs_page_url': 'http://www.jobscore.com/jobs/orchestrate/',

    'empcnt': [11,50]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
