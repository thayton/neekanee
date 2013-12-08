from neekanee.jobscrapers.taleo.taleo2 import TaleoJobScraper

COMPANY = {
    'name': 'Unilever',
    'hq': 'London, England',

    'home_page_url': 'http://www.unilever.com',
    'jobs_page_url': 'https://unilever.taleo.net/careersection/external/jobsearch.ftl?lang=en&portal=6170030171',

    'empcnt': [10001]
}

class UnileverNetJobScraper(TaleoJobScraper):
    def __init__(self):
        super(UnileverNetJobScraper, self).__init__(COMPANY)

def get_scraper():
    return UnileverNetJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
