from neekanee.jobscrapers.workable.workable import WorkableJobScraper

COMPANY = {
    'name': 'Mindworks Interactive',
    'hq': 'Acharnes, Attiki, Greece',

    'home_page_url': 'http://www.mindworks.gr',
    'jobs_page_url': 'http://mindworks.workable.com',

    'empcnt': [11,50]
}

def get_scraper():
    return WorkableJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
