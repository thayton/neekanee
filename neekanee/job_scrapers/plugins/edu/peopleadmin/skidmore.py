from neekanee.jobscrapers.peopleadmin.PeopleAdminATS import PeopleAdminJobScraper

COMPANY = {
    'name': 'Skidmore College',
    'hq': 'Saratoga Springs, NY',

    'benefits': {
        'url': 'http://cms.skidmore.edu/hr/benefits/index.cfm',
        'vacation': [],
        'holidays': 14,
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.skidmore.edu',
    'jobs_page_url': 'https://careers.skidmore.edu/applicants/jsp/shared/Welcome_css.jsp',

    'empcnt': [501,1000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
