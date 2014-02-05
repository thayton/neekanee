from neekanee.jobscrapers.workable.workable import WorkableJobScraper

COMPANY = {
    'name': 'Netrobe',
    'hq': 'Athens, Attiki, Greece',

    'home_page_url': 'http://www.netrobe.com',
    'jobs_page_url': 'http://netrobe.workable.com',

    'empcnt': [1,10]
}

def get_scraper():
    return WorkableJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
