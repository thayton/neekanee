from neekanee.jobscrapers.taleo.taleo2 import TaleoJobScraper

COMPANY = {
    'name': 'Edwards',
    'hq': 'Irvine, CA',

    'home_page_url': 'http://www.edwards.com',
    'jobs_page_url': 'https://edwards.taleo.net/careersection/edwards_external_cs/jobsearch.ftl?lang=en',

    'empcnt': [5001, 10000]
}

class EdwardsJobScraper(TaleoJobScraper):
    def __init__(self):
        super(EdwardsJobScraper, self).__init__(COMPANY)

def get_scraper():
    return EdwardsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
