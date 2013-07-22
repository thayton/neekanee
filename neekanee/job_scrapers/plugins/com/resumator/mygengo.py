from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'myGengo',
    'hq': 'Tokyo, Japan',

    'home_page_url': 'http://mygengo.com',
    'jobs_page_url': 'http://gengo.theresumator.com',

    'empcnt': [11,50]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()

