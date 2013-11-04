from neekanee.jobscrapers.taleo.taleo2 import TaleoJobScraper

COMPANY = {
    'name': 'CSX',
    'hq': 'Jacksonville, FL',

    'home_page_url': 'http://www.csx.com',
    'jobs_page_url': 'https://csx.taleo.net/careersection/2/moresearch.ftl?lang=en',

    'empcnt': [10001]
}

class CsxNetJobScraper(TaleoJobScraper):
    def __init__(self):
        super(CsxNetJobScraper, self).__init__(COMPANY)

def get_scraper():
    return CsxNetJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
