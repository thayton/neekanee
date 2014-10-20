from neekanee.jobscrapers.cats.cats import CatsJobScraper
from location import parse_location

COMPANY = {
    'name': 'Trace Systems',
    'hq': 'McLean, VA',

    'home_page_url': 'http://www.tracesystems.com',
    'jobs_page_url': 'http://trace.catsone.com/careers/index.php',

    'empcnt': [51,200]
}

def get_scraper():
    return CatsJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
