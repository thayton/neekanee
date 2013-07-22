from neekanee.jobscrapers.peopleadmin.PeopleAdminATS import PeopleAdminJobScraper

COMPANY = {
    'name': 'Bucknell University',
    'hq': 'Lewisburg, PA',

    'benefits': {
        'url': 'http://www.bucknell.edu/x4948.xml',
        'vacation': [],
        'holidays': 12,
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.bucknell.edu',
    'jobs_page_url': 'https://jobs.bucknell.edu/applicants/jsp/shared/Welcome_css.jsp',

    'empcnt': [1001,5000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
