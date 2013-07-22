from neekanee.jobscrapers.peopleadmin.peopleadmin2 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Salem State University',
    'hq': 'Salem, MA',

    'home_page_url': 'http://www.salemstate.edu',
    'jobs_page_url': 'https://jobs.salemstate.edu/applicants/jsp/shared/index.jsp',

    'gctw_chronicle': True,

    'empcnt': [1001,5000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
