from neekanee.jobscrapers.lever.lever import LeverJobScraper

COMPANY = {
    'name': 'Shopify',
    'hq': 'Ottawa, Canada',

    'home_page_url': 'http://www.shopify.com',
    'jobs_page_url': 'https://jobs.lever.co/shopify/',

    'empcnt': [201,500]
}

def get_scraper():
    return LeverJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
