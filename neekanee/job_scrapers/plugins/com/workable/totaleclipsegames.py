from neekanee.jobscrapers.workable.workable import WorkableJobScraper

COMPANY = {
    'name': 'Total Eclipse',
    'hq': 'Pylaia Thessaloniki, Greece',

    'home_page_url': 'http://www.totaleclipsegames.com',
    'jobs_page_url': 'http://totaleclipse.workable.com',

    'empcnt': [1,10]
}

def get_scraper():
    return WorkableJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
