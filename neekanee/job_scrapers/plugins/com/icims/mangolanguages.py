from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'Mango Languages',
    'hq': 'Farmington Hills, MI',

    'home_page_url': 'http://www.mangolanguages.com',
    'jobs_page_url': 'https://jobs-mangolanguages.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [51,200]
}

class MangoLanguagesJobScraper(IcimsJobScraper):
    def __init__(self):
        super(MangoLanguagesJobScraper, self).__init__(COMPANY)

def get_scraper():
    return MangoLanguagesJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()

