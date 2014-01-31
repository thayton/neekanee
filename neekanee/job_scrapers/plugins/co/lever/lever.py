from neekanee.jobscrapers.lever.lever import LeverJobScraper

COMPANY = {
    'name': 'Lever',
    'hq': 'San Francisco, CA',

    'home_page_url': 'https://lever.co',
    'jobs_page_url': 'https://jobs.lever.co/lever',

    'empcnt': [1,10]
}

def get_scraper():
    return LeverJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
