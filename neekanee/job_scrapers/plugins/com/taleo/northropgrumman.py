from neekanee.jobscrapers.taleo.taleo2 import TaleoJobScraper

COMPANY = {
    'name': 'Northrop Grumman',
    'hq': 'Falls Church, VA',

    'home_page_url': 'http://www.northropgrumman.com',
    'jobs_page_url': 'https://ngc.taleo.net/careersection/ngc_pro/jobsearch.ftl?lang=en',

    'empcnt': [10001]
}

class NorthropGrummanNetJobScraper(TaleoJobScraper):
    def __init__(self):
        super(NorthropGrummanNetJobScraper, self).__init__(COMPANY)

def get_scraper():
    return NorthropGrummanNetJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
