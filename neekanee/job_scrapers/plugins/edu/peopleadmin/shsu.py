from neekanee.jobscrapers.peopleadmin.peopleadmin3 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Sam Houston State University',
    'hq': 'Huntsville, TX',

    'benefits': {
        'url': 'http://www.shsu.edu/~hrd_www/benefits/',
        'vacation': [(1,12),(2,13.5),(5,15),(10,16.5),(15,19.5),(20,22.5),(25,25.5),(30,28.5),(35,31.5)],
        'holidays': 13,
        'sick_days': 12
    },

    'home_page_url': 'http://www.shsu.edu',
    'jobs_page_url': 'https://shsu.peopleadmin.com',

    'gctw_chronicle': True,

    'empcnt': [1001,5000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
