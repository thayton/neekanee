from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'FIRST',
    'hq': 'Manchester, NH',

    'ats': 'icims',

    'home_page_url': 'http://www.first.org',
    'jobs_page_url': 'https://jobs-usfirst.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [51,200]
}

class FirstJobScraper(IcimsJobScraper):
    def __init__(self):
        super(FirstJobScraper, self).__init__(COMPANY)

def get_scraper():
    return FirstJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
