from neekanee.jobscrapers.workable.workable import WorkableJobScraper

COMPANY = {
    'name': 'Beintoo',
    'hq': 'Milan, Italy',

    'home_page_url': 'http://www.beintoo.com',
    'jobs_page_url': 'http://beintoo.workable.com',

    'empcnt': [11,50]
}

def get_scraper():
    return WorkableJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
