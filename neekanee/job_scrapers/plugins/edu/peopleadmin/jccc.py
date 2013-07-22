from neekanee.jobscrapers.peopleadmin.peopleadmin2 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Johnson County Community College',
    'hq': 'Overland Park, KS',

    'benefits': {
        'url': 'http://www.jccc.edu/human-resources/employee-benefits/index.html',
        'vacation': [(1,18),(10,20),(15,22),(20,24)],
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.jccc.edu',
    'jobs_page_url': 'https://jobs.jccc.edu/applicants/jsp/shared/index.jsp',

    'gctw_chronicle': True,

    'empcnt': [1001,5000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
