from neekanee.jobscrapers.taleo.taleo2 import TaleoJobScraper

COMPANY = {
    'name': 'Vanderbilt University',
    'hq': 'Nashville, TN',

    'home_page_url': 'http://www.vanderbilt.edu',
    'jobs_page_url': 'https://vanderbilt.taleo.net/careersection/.vu_cs/jobsearch.ftl',

    'empcnt': [10001]
}

class VanderbiltJobScraper(TaleoJobScraper):
    def __init__(self):
        super(VanderbiltJobScraper, self).__init__(COMPANY)
        
def get_scraper():
    return VanderbiltJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
