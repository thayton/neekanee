from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'Aramark',
    'hq': 'Philadelphia, PA',

    'home_page_url': 'http://www.aramark.com',
    'jobs_page_url': 'https://allcareers-aramark.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [10001]
}

class AramarkJobScraper(IcimsJobScraper):
    def __init__(self):
        super(AramarkJobScraper, self).__init__(COMPANY)

def get_scraper():
    return AramarkJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
