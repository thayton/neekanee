from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': '360pi',
    'hq': 'Ottawa, Canada',

    'home_page_url': 'http://www.360pi.com',
    'jobs_page_url': 'http://360pi.theresumator.com',

    'empcnt': [11,50]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
