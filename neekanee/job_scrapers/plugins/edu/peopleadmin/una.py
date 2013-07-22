from neekanee.jobscrapers.peopleadmin.peopleadmin2 import PeopleAdminJobScraper

COMPANY = {
    'name': 'University of Northern Alabama',
    'hq': 'Florence, AL',

    'benefits': {
        'url': 'http://www.una.edu/humanresources/benefits/',
        'vacation': [],
        'holidays': 25,
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.una.edu',
    'jobs_page_url': 'https://jobs.una.edu/applicants/jsp/shared/index.jsp',

    'empcnt': [201,500]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
