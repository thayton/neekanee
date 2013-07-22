from neekanee.jobscrapers.peopleadmin.peopleadmin3 import PeopleAdminJobScraper

COMPANY = {
    'name': 'University of Florida',
    'hq': 'Gainesville, FL',

    'benefits': {
        'url': 'http://www.hr.ufl.edu/benefits/default.asp',
        'vacation': [(1,13),(6,16),(11,19)],
        'holidays': 10,
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.ufl.edu',
    'jobs_page_url': 'https://jobs.ufl.edu',

    'empcnt': [10001]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
