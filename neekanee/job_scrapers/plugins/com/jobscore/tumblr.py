from neekanee.jobscrapers.jobscore.jobscore2 import JobScoreJobScraper

COMPANY = {
    'name': 'Tumblr',
    'hq': 'New York, NY',

    'home_page_url': 'http://www.tumblr.com',
    'jobs_page_url': 'http://www.jobscore.com/jobs2/tumblr/',

    'empcnt': [51,200]
}

def get_scraper():
    return JobScoreJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
