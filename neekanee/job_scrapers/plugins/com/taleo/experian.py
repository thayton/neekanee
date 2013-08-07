from neekanee.jobscrapers.taleo.taleo2 import TaleoJobScraper

COMPANY = {
    'name': 'Experian',
    'hq': 'Costa Mesa, CA',

    'home_page_url': 'http://www.experian.com',
    'jobs_page_url': 'https://experian.taleo.net/careersection/2/jobsearch.ftl',

    'empcnt': [10001]
}

class ExperianJobScraper(TaleoJobScraper):
    def __init__(self):
        super(ExperianJobScraper, self).__init__(COMPANY)

def get_scraper():
    return ExperianJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
