from neekanee.jobscrapers.taleo.taleo2 import TaleoJobScraper

COMPANY = {
    'name': 'Occidental Petroleum Corporation (Oxy)',
    'hq': 'Los Angeles, CA',

    'home_page_url': 'http://www.oxy.com',
    'jobs_page_url': 'https://oxy.taleo.net/careersection/2/jobsearch.ftl?lang=en',

    'empcnt': [10001]
}

class OxyJobScraper(TaleoJobScraper):
    def __init__(self):
        super(OxyJobScraper, self).__init__(COMPANY)

def get_scraper():
    return OxyJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
