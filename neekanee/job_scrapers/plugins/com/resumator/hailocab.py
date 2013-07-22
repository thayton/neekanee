from neekanee.jobscrapers.resumator.resumator3 import ResumatorJobScraper

COMPANY = {
    'name': 'Hailo',
    'hq': 'London, UK',

    'home_page_url': 'https://www.hailocab.com',
    'jobs_page_url': 'http://hailo.theresumator.com',

    'empcnt': [51,200]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
