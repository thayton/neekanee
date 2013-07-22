from neekanee.jobscrapers.resumator.resumator2 import ResumatorJobScraper

COMPANY = {
    'name': 'Bonobos',
    'hq': 'New York, NY',

    'home_page_url': 'http://www.bonobos.com',
    'jobs_page_url': 'http://bonobos.theresumator.com',

    'empcnt': [51,200]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
