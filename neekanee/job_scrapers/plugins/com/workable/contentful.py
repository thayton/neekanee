from neekanee.jobscrapers.workable.workable import WorkableJobScraper

COMPANY = {
    'name': 'Contentful',
    'hq': 'Berlin, Germany',

    'home_page_url': 'http://www.contentful.com',
    'jobs_page_url': 'http://contentful.workable.com',

    'empcnt': [1,10]
}

def get_scraper():
    return WorkableJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
