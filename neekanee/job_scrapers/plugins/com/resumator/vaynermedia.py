from neekanee.jobscrapers.resumator.resumator2 import ResumatorJobScraper

COMPANY = {
    'name': 'VaynerMedia',
    'hq': 'New York, NY',

    'home_page_url': 'http://www.vaynermedia.com',
    'jobs_page_url': 'http://vaynermedia.theresumator.com',

    'empcnt': [11,50]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
