from neekanee.jobscrapers.peopleadmin.peopleadmin2 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Eastern Kentucky University',
    'hq': 'Richmond, KY',

    'benefits': {
        'url': 'http://www.hr.eku.edu/benefits/',
        'vacation': []
    },

    'home_page_url': 'http://www.eku.edu',
    'jobs_page_url': 'https://jobs.eku.edu/applicants/jsp/shared/index.jsp',

    'gctw_chronicle': True,

    'empcnt': [1001,5000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
