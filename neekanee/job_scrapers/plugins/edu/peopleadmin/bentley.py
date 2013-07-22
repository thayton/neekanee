from neekanee.jobscrapers.peopleadmin.peopleadmin2 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Bentley University',
    'hq': 'Waltham, MA',

    'benefits': {
        'url': 'http://legacy.bentley.edu/hr/benefits/index.cfm',
        'vacation':[]
    },

    'home_page_url': 'http://www.bentley.edu',
    'jobs_page_url': 'https://jobs.bentley.edu/applicants/jsp/shared/index.jsp',

    'empcnt': [501,1000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
