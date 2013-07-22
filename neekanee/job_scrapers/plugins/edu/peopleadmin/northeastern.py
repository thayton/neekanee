from neekanee.jobscrapers.peopleadmin.peopleadmin3 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Northeastern University',
    'hq': 'Boston, MA',

    'home_page_url': 'http://www.northeastern.edu',
    'jobs_page_url': 'https://neu.peopleadmin.com/',

    'empcnt': [1001,5000]
}

class NortheasternJobScraper(PeopleAdminJobScraper):
    def __init__(self):
        super(NortheasternJobScraper, self).__init__(COMPANY)

def get_scraper():
    return NortheasternJobScraper()
