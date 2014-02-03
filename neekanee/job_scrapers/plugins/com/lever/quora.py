from neekanee.jobscrapers.lever.lever import LeverJobScraper

COMPANY = {
    'name': 'Quora',
    'hq': 'Palo Alto, CA',

    'home_page_url': 'http://www.quora.com',
    'jobs_page_url': 'https://jobs.lever.co/quora',

    'empcnt': [1,10]
}

def get_scraper():
    return LeverJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
