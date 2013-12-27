from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'Rapid7',
    'hq': 'Boston, MA',

    'home_page_url': 'http://www.rapid7.com',
    'jobs_page_url': 'https://careers-rapid7.icims.com/jobs/intro?hashed=0&in_iframe=1',

    'empcnt': [201,500]
}

def get_scraper():
    return IcimsJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
