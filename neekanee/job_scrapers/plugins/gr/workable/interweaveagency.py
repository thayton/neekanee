from neekanee.jobscrapers.workable.workable import WorkableJobScraper

COMPANY = {
    'name': 'Interweave Agency',
    'hq': 'Athens, Greece',

    'home_page_url': 'http://www.interweaveagency.gr',
    'jobs_page_url': 'http://interweave.workable.com',

    'empcnt': [11,50]
}

def get_scraper():
    return WorkableJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
