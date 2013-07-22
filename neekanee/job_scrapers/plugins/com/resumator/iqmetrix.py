from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'IQmetrix',
    'hq': 'Vancouver, Canada',

    'home_page_url': 'http://www.iqmetrix.com',
    'jobs_page_url': 'http://iqmetrix.theresumator.com',

    'empcnt': [201,500]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
