from neekanee.jobscrapers.peopleadmin.PeopleAdminATS import PeopleAdminJobScraper

COMPANY = {
    'name': 'University of Notre Dame',
    'hq': 'Notre Dame, IN',

    'benefits': {
        'url': 'http://hr.nd.edu/benefits/',
        'vacation': [(1,10),(3,15),(11,20),(21,25)],
        'holidays': 12,
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.nd.edu',
    'jobs_page_url': 'https://jobs.nd.edu/applicants/jsp/shared/Welcome_css.jsp',

    'gctw_chronicle': True,

    'empcnt': [1001,5000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
