from neekanee.jobscrapers.workable.workable import WorkableJobScraper

COMPANY = {
    'name': 'VisionMobile',
    'hq': 'London, England',

    'home_page_url': 'http://www.visionmobile.com',
    'jobs_page_url': 'http://visionmobile.workable.com',

    'empcnt': [1,10]
}

def get_scraper():
    return WorkableJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
