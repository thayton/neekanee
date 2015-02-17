from neekanee.jobscrapers.lever.lever import LeverJobScraper

COMPANY = {
    'name': 'Triggit',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://triggit.com',
    'jobs_page_url': 'https://jobs.lever.co/triggit',

    'empcnt': [11,50]
}

def get_scraper():
    return LeverJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
