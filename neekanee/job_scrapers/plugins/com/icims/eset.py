from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'ESET',
    'hq': 'Bratislava, Slovak Republic',

    'home_page_url': 'http://www.eset.com',
    'jobs_page_url': 'https://globalcareers-eset.icims.com/jobs/intro?hashed=0&in_iframe=1',

    'empcnt': [1001,5000]
}

def get_scraper():
    return IcimsJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
