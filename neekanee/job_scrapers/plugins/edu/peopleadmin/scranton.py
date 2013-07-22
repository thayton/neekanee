from neekanee.jobscrapers.peopleadmin.PeopleAdminATS import PeopleAdminJobScraper

COMPANY = {
    'name': 'University of Scranton',
    'hq': 'Scranton, PA',
        
    'benefits': {
        'url': 'http://matrix.scranton.edu/humanresources/hr_benefits.shtml',
        'vacation': [],
        'holidays': 15,
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.scranton.edu',
    'jobs_page_url': 'https://universityofscrantonjobs.com/applicants/jsp/shared/Welcome_css.jsp',

    'empcnt': [1001,5000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
