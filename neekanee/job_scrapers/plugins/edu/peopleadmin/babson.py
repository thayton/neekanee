from neekanee.jobscrapers.peopleadmin.peopleadmin3 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Babson College',
    'hq': 'Babson Park, MA',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.babson.edu',
    'jobs_page_url': 'https://babson.peopleadmin.com',

    'gctw_chronicle': True,

    'empcnt': [501,1000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
