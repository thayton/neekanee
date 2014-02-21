from neekanee.jobscrapers.taleo.taleo2 import TaleoJobScraper

COMPANY = {
    'name': 'Johns Hopkins Applied Physics Laboratory',
    'hq': 'Laurel, MD',

    'home_page_url': 'http://www.jhuapl.edu',
    'jobs_page_url': 'https://jhuapl.taleo.net/careersection/2/moresearch.ftl',

    'empcnt': [1001,5000]
}

class JhuAplJobScraper(TaleoJobScraper):
    def __init__(self):
        super(JhuAplJobScraper, self).__init__(COMPANY)
        
def get_scraper():
    return JhuAplJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
