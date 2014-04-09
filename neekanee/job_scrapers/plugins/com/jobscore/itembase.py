from neekanee.jobscrapers.jobscore.jobscore2 import JobScoreJobScraper

COMPANY = {
    'name': 'Itembase',
    'hq': 'Berlin, Germany',

    'home_page_url': 'http://www.itembase.com',
    'jobs_page_url': 'https://www.jobscore.com/jobs/itembase/ ',

    'empcnt': [11,50]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
