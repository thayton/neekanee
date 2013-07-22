from neekanee.jobscrapers.peopleadmin.PeopleAdminATS import PeopleAdminJobScraper

COMPANY = {
    'name': 'Georgia Perimeter College',
    'hq': 'Covington, GA',

    'benefits': {
        'url': 'http://www.gpc.edu/humanresources/content/benefits-and-retirement',
        'vacation': [(1,15),(6,18),(11,21)],
        'sick_leave': 12,
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.gpc.edu',
    'jobs_page_url': 'https://careers.gpc.edu/applicants/jsp/shared/Welcome_css.jsp',

    'empcnt': [1001,5000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
