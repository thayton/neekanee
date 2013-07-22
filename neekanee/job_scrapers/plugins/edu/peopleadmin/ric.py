from neekanee.jobscrapers.peopleadmin.PeopleAdminATS import PeopleAdminJobScraper

COMPANY = {
    'name': 'Rhode Island College',
    'hq': 'Providence, RI',

    'benefits': {
        'vacation': [(1,22)],
        'holidays': 10,
        'sick_days': 15,
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.ric.edu',
    'jobs_page_url': 'https://employment.ric.edu/applicants/jsp/shared/Welcome_css.jsp',

    'empcnt': [501,1000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
