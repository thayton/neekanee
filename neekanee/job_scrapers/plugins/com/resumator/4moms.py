from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': '4moms',
    'hq': 'Pittsburgh, PA',

    'home_page_url': 'http://www.4moms.com',
    'jobs_page_url': 'http://4moms.theresumator.com',

    'empcnt': [11,50]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
