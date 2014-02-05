from neekanee.jobscrapers.workable.workable import WorkableJobScraper

COMPANY = {
    'name': 'Existanze Integrated Solutions',
    'hq': 'Paraskevi, Attiki, Greece',

    'home_page_url': 'http://www.existanze.com',
    'jobs_page_url': 'http://existanze.workable.com',

    'empcnt': [1,10]
}

def get_scraper():
    return WorkableJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
