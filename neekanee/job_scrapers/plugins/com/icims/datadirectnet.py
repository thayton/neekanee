from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'DataDirect Networks',
    'hq': 'Chatsworth, CA',

    'home_page_url': 'http://www.ddn.com',
    'jobs_page_url': 'https://careers-ddn.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [201,500]
}

class DataDirectNetJobScraper(IcimsJobScraper):
    def __init__(self):
        super(DataDirectNetJobScraper, self).__init__(COMPANY)

def get_scraper():
    return DataDirectNetJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
