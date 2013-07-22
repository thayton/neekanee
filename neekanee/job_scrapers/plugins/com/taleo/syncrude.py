from neekanee.jobscrapers.taleo.taleo2 import TaleoJobScraper

COMPANY = {
    'name': 'Syncrude Canada',
    'hq': 'Fort McMurray, Canada',

    'home_page_url': 'http://www.syncrude.ca/',
    'jobs_page_url': 'http://syncrude.taleo.net/careersection/2/jobsearch.ftl?lang=en',

    'empcnt': [5001,10000]
}

class SyncrudeJobScraper(TaleoJobScraper):
    def __init__(self):
        super(SyncrudeJobScraper, self).__init__(COMPANY)

def get_scraper():
    return SyncrudeJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
