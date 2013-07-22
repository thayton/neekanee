from neekanee.jobscrapers.peopleadmin.peopleadmin3 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Southern New Hampshire University',
    'hq': 'Manchester, NH',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.snhu.edu',
    'jobs_page_url': 'https://snhu.peopleadmin.com',

    'gctw_chronicle': True,

    'empcnt': [501,1000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
