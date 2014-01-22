from neekanee.jobscrapers.peopleadmin.peopleadmin3 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Wesleyan University',
    'hq': 'Hartford, Connecticut',

    'home_page_url': 'http://www.wesleyan.edu/',
    'jobs_page_url': 'https://careers.wesleyan.edu/',

    'empcnt': [201,500]
}

class WaltersStateJobScraper(PeopleAdminJobScraper):
    def __init__(self):
        super(WaltersStateJobScraper, self).__init__(COMPANY)

def get_scraper():
    return WaltersStateJobScraper()

if __name__:
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
