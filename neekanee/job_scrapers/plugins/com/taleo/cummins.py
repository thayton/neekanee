from neekanee.jobscrapers.taleo.taleo2 import TaleoJobScraper

COMPANY = {
    'name': 'Cummins',
    'hq': 'Columbus, IN',

    'ats': 'Taleo',

    'home_page_url': 'http://www.cummins.com',
    'jobs_page_url': 'https://cummins.taleo.net/careersection/cmicareersection_external_professional/moresearch.ftl?lang=en',

    'empcnt': [10001]
}

class CumminsJobScraper(TaleoJobScraper):
    def __init__(self):
        super(CumminsJobScraper, self).__init__(COMPANY)

def get_scraper():
    return CumminsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
