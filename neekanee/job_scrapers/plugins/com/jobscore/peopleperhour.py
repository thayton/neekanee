from neekanee.jobscrapers.jobscore.jobscore2 import JobScoreJobScraper

COMPANY = {
    'name': 'PeoplePerHour.com',
    'hq': 'London, England',

    'home_page_url': 'http://www.peopleperhour.com',
    'jobs_page_url': 'http://www.jobscore.com/jobs/peopleperhourcom/',

    'empcnt': [11,50]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
