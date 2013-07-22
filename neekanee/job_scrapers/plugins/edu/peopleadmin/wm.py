from neekanee.jobscrapers.peopleadmin.peopleadmin3 import PeopleAdminJobScraper

COMPANY = {
    'name': 'College of William and Marry',
    'hq': 'Williamsburg, VA',

    'home_page_url': 'http://www.wm.edu/',
    'jobs_page_url': 'https://jobs.wm.edu',

    'empcnt': [1001,5000]
}

class WmJobScraper(PeopleAdminJobScraper):
    def __init__(self):
        super(WmJobScraper, self).__init__(COMPANY)

def get_scraper():
    return WmJobScraper()

if __name__:
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
