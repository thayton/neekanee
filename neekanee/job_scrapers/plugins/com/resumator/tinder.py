from neekanee.jobscrapers.resumator.resumator2 import ResumatorJobScraper

COMPANY = {
    'name': 'Tinder',
    'hq': 'Los Angeles, CA',

    'home_page_url': 'http://www.tinder.com',
    'jobs_page_url': 'http://tinder.theresumator.com',

    'empcnt': [51,200]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
