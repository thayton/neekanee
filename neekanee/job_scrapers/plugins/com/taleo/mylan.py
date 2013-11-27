from neekanee.jobscrapers.taleo.taleo2 import TaleoJobScraper

COMPANY = {
    'name': 'Mylan',
    'hq': 'Canonsburg, PA',

    'home_page_url': 'http://www.mylan.com',
    'jobs_page_url': 'https://mylan.taleo.net/careersection/myl_usajobs/jobsearch.ftl?lang=en',

    'empcnt': [10001]
}

class MylanNetJobScraper(TaleoJobScraper):
    def __init__(self):
        super(MylanNetJobScraper, self).__init__(COMPANY)

def get_scraper():
    return MylanNetJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
