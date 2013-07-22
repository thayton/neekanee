from neekanee.jobscrapers.peopleadmin.PeopleAdminATS import PeopleAdminJobScraper

COMPANY = {
    'name': 'Northern Kentucky University',
    'hq': 'Highland Heights, KY',

    'benefits': {
        'url': 'http://hr.nku.edu/benefits/index.php',
        'vacation': [(1,20),(10,25)],
        'holidays': 8,
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.nku.edu',
    'jobs_page_url': 'https://jobs.nku.edu/applicants/jsp/shared/Welcome_css.jsp',

    'empcnt': [1001,5000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
