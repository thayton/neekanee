from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Bondsy',
    'hq': 'Brooklyn, NY',

    'home_page_url': 'http://www.bondsy.com',
    'jobs_page_url': 'http://bondsy.theresumator.com',

    'empcnt': [1,10]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
