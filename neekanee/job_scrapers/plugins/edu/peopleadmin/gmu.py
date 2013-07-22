from neekanee.jobscrapers.peopleadmin.peopleadmin3 import PeopleAdminJobScraper

COMPANY = {
    'name': 'George Mason University',
    'hq': 'Fairfax, VA',

    'benefits': {
        'url': 'http://hr.gmu.edu/benefits/',
        'vacation': [(1,12),(6,15),(11,18),(22,21),(26,27)],
        'holidays': 12
    },

    'home_page_url': 'http://www.gmu.edu',
    'jobs_page_url': 'https://jobs.gmu.edu',

    'gctw_chronicle': True,

    'empcnt': [1001,5000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
