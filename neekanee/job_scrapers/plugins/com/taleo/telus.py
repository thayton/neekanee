from neekanee.jobscrapers.taleo.taleo2 import TaleoJobScraper

COMPANY = {
    'name': 'Telus',
    'hq': 'Vancouver, Canada',

    'home_page_url': 'http://www.telus.com',
    'jobs_page_url': 'https://telus.taleo.net/careersection/10000/jobsearch.ftl?lang=en',

    'empcnt': [10001]
}

class TelusNetJobScraper(TaleoJobScraper):
    def __init__(self):
        super(TelusNetJobScraper, self).__init__(COMPANY)

def get_scraper():
    return TelusNetJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
