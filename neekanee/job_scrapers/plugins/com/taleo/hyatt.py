from neekanee.jobscrapers.taleo.taleo2 import TaleoJobScraper

COMPANY = {
    'name': 'Hyatt Hotels Corporation',
    'hq': 'Chicago, IL',

    'home_page_url': 'http://www.hyatt.com',
    'jobs_page_url': 'https://hyatt.taleo.net/careersection/10880/jobsearch.ftl?lang=en&src=CWS-1&searchExpand=false',

    'empcnt': [10001]
}

class HyattNetJobScraper(TaleoJobScraper):
    def __init__(self):
        super(HyattNetJobScraper, self).__init__(COMPANY)

def get_scraper():
    return HyattNetJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
