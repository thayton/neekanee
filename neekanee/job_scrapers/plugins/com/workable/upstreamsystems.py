from neekanee.jobscrapers.workable.workable import WorkableJobScraper

COMPANY = {
    'name': 'Upstream Systems',
    'hq': 'London, England',

    'home_page_url': 'http://www.upstreamsystems.com',
    'jobs_page_url': 'http://upstream.workable.com',

    'empcnt': [51,200]
}

def get_scraper():
    return WorkableJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
