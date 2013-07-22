from neekanee.jobscrapers.peopleadmin.PeopleAdminATS import PeopleAdminJobScraper

COMPANY = {
    'name': 'University of Minnesota',
    'hq': 'Minneapolis, MN',

    'benefits': {
        'url': 'http://www1.umn.edu/ohr/benefits/index.html',
        'vacation': [],
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.umn.edu',
    'jobs_page_url': 'https://employment.umn.edu/applicants/jsp/shared/Welcome_css.jsp',

    'empcnt': [10001]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
