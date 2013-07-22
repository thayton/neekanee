from neekanee.jobscrapers.peopleadmin.peopleadmin2 import PeopleAdminJobScraper

COMPANY = {
    'name': 'California State University Channel Islands',
    'hq': 'Camarillo, CA',

    'benefits': {
        'url': 'http://www.csuci.edu/hr/benefits.htm',
        'vacation': []
    },

    'home_page_url': 'http://www.csuci.edu',
    'jobs_page_url': 'https://www.csucijobs.com/applicants/jsp/shared/index.jsp',

    'gctw_chronicle': True,

    'empcnt': [201,500]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
