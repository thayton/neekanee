from neekanee.jobscrapers.taleo.taleo2 import TaleoJobScraper

COMPANY = {
    'name': 'Chesapeake Energy',
    'hq': 'Oklahoma City, OK',

    'home_page_url': 'http://www.chk.com',
    'jobs_page_url': 'https://chk.taleo.net/careersection/2/jobsearch.ftl?lang=en',

    'empcnt': [10001]
}

class ChkJobScraper(TaleoJobScraper):
    def __init__(self):
        super(ChkJobScraper, self).__init__(COMPANY)

def get_scraper():
    return ChkJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
