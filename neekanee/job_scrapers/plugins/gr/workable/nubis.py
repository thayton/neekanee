from neekanee.jobscrapers.workable.workable import WorkableJobScraper

COMPANY = {
    'name': 'Nubis',
    'hq': 'Kallithea, Athens, Greece',

    'home_page_url': 'http://www.nubis.gr',
    'jobs_page_url': 'http://nubis-sa.workable.com',

    'empcnt': [11,50]
}

def get_scraper():
    return WorkableJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
