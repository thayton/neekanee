from neekanee.jobscrapers.resumator.resumator2 import ResumatorJobScraper

COMPANY = {
    'name': 'OkCupid',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.okcupid.com',
    'jobs_page_url': 'http://okcupid.theresumator.com',

    'empcnt': [11,50]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
