from neekanee.jobscrapers.peopleadmin.PeopleAdminATS import PeopleAdminJobScraper

COMPANY = {
    'name': 'Wellesley College',
    'hq': 'Wellesley, MA',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.wellesley.edu',
    'jobs_page_url': 'https://career.wellesley.edu/applicants/jsp/shared/Welcome_css.jsp',

    'gctw_chronicle': True,

    'empcnt': [501,1000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
