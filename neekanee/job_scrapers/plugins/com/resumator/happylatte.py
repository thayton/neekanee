from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Happylatte',
    'hq': 'Beijing, China',

    'home_page_url': 'http://www.happylatte.com',
    'jobs_page_url': 'http://happylatte.theresumator.com',

    'empcnt': [51,200]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
