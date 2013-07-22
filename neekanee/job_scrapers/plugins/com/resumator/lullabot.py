from neekanee.jobscrapers.resumator.resumator2 import ResumatorJobScraper

COMPANY = {
    'name': 'Lullabot',
    'hq': 'Providence, RI',

    'home_page_url': 'http://www.lullabot.com',
    'jobs_page_url': 'http://lullabot.theresumator.com',

    'empcnt': [11,50]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
