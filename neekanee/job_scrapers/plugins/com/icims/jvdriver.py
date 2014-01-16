from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'JV Driver Projects',
    'hq': 'Leduc, Canada',

    'home_page_url': 'http://www.jvdriver.com',
    'jobs_page_url': 'https://careers-jvdriver.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [1001,5000]
}

class JvDriverJobScraper(IcimsJobScraper):
    def __init__(self):
        super(JvDriverJobScraper, self).__init__(COMPANY)

def get_scraper():
    return JvDriverJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
