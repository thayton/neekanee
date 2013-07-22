from neekanee.jobscrapers.taleo.taleo2 import TaleoJobScraper

COMPANY = {
    'name': 'Nabors Industries',
    'hq': 'Hamilton, Bermuda',

    'home_page_url': 'http://www.nabors.com',
    'jobs_page_url': 'https://nabors.taleo.net/careersection/02/moresearch.ftl?lang=en',

    'empcnt': [10001]
}

class NaborsJobScraper(TaleoJobScraper):
    def __init__(self):
        super(NaborsJobScraper, self).__init__(COMPANY)

def get_scraper():
    return NaborsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
