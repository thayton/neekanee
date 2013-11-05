from neekanee.jobscrapers.taleo.taleo2 import TaleoJobScraper

COMPANY = {
    'name': 'Klein Associates, Inc',
    'hq': 'Salem, NH',

    'home_page_url': 'http://www.l-3klein.com',
    'jobs_page_url': 'https://l3com.taleo.net/careersection/l3_ext_us/jobsearch.ftl?lang=en',

    'empcnt': [11,50],
}

class KleinJobScraper(TaleoJobScraper):
    def __init__(self):
        super(KleinJobScraper, self).__init__(COMPANY)

def get_scraper():
    return KleinJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
