from neekanee.jobscrapers.workable.workable import WorkableJobScraper

COMPANY = {
    'name': 'Echoing Green',
    'hq': 'New York, NY',

    'home_page_url': 'http://www.echoinggreen.com',
    'jobs_page_url': 'http://echoing-green.workable.com',

    'empcnt': [11,50]
}

def get_scraper():
    return WorkableJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
