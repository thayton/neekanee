from neekanee.jobscrapers.peopleadmin.peopleadmin3 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Dean College',
    'hq': 'Franklin, MA',

    'home_page_url': 'http://www.dean.edu/',
    'jobs_page_url': 'https://dean.peopleadmin.com/',

    'empcnt': [201,500]
}

class DeanJobScraper(PeopleAdminJobScraper):
    def __init__(self):
        super(DeanJobScraper, self).__init__(COMPANY)

def get_scraper():
    return DeanJobScraper()
