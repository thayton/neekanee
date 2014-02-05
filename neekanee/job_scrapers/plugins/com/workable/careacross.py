from neekanee.jobscrapers.workable.workable import WorkableJobScraper

COMPANY = {
    'name': 'CareAcross',
    'hq': 'Marousi, Attiki, Greece',

    'home_page_url': 'http://www.careacross.com',
    'jobs_page_url': 'http://careacross.workable.com',

    'empcnt': [1,10]
}

def get_scraper():
    return WorkableJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
