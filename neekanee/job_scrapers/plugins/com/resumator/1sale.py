from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': '1Sale.com',
    'hq': 'Miami, FL',

    'home_page_url': 'http://www.1sale.com',
    'jobs_page_url': 'http://1sale.theresumator.com',

    'empcnt': [51,200]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
