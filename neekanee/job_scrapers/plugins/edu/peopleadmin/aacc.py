from neekanee.jobscrapers.peopleadmin.peopleadmin2 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Anne Arundel Community College',
    'hq': 'Arnold, MD',

    'benefits': {
        'url': 'http://www.aacc.edu/employment/benefits1.cfm',
        'vacation': [(1,15),(6,22)],
        'sick_days': 15,
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.aacc.edu',
    'jobs_page_url': 'https://careers.aacc.edu/applicants/jsp/shared/index.jsp',

    'gctw_chronicle': True,

    'empcnt': [501,1000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
