from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Audicus',
    'hq': 'Hoboken, NJ',

    'home_page_url': 'http://www.audicus.com',
    'jobs_page_url': 'http://audicus.theresumator.com',

    'empcnt': [1,10]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
