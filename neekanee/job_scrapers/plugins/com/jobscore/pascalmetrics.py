from neekanee.jobscrapers.jobscore.jobscore import JobScoreJobScraper

COMPANY = {
    'name': 'Pascal Metrics',
    'hq': 'Washington, DC',

    'home_page_url': 'http://www.pascalmetrics.com/',
    'jobs_page_url': 'http://www.jobscore.com/jobs/pascalmetrics/list',

    'empcnt': [501,1000]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
