from neekanee.jobscrapers.lever.lever import LeverJobScraper

COMPANY = {
    'name': 'Standard Treasury',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.standardtreasury.com',
    'jobs_page_url': 'https://jobs.lever.co/standardtreasury',

    'empcnt': [1,10]
}

def get_scraper():
    return LeverJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
