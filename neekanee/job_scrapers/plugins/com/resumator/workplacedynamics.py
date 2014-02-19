from neekanee.jobscrapers.resumator.resumator import ResumatorJobScraper

COMPANY = {
    'name': 'Workplace Dynamics',
    'hq': 'Exton, PA',

    'home_page_url': 'http://www.workplacedynamics.com',
    'jobs_page_url': 'http://workplacedynamics.theresumator.com',

    'empcnt': [11,50]
}

def get_scraper():
    return ResumatorJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
