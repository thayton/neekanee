from neekanee.jobscrapers.peopleadmin.peopleadmin2 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Colby-Sawyer College',
    'hq': 'New London, NH',

    'benefits': {
        'url': 'http://www.colby-sawyer.edu/people-offices/hr/benefits.html',
        'vacation': [(1,20)],
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.colby-sawyer.edu',
    'jobs_page_url': 'https://colby-sawyer.simplehire.com/applicants/jsp/shared/index.jsp',

    'gctw_chronicle': True,

    'empcnt': [501,1000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
