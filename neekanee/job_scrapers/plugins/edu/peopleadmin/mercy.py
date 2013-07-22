from neekanee.jobscrapers.peopleadmin.PeopleAdminATS import PeopleAdminJobScraper

COMPANY = {
    'name': 'Mercy College',
    'hq': 'Dobbs Ferry, NY',

    'benefits': {
        'url': 'https://www.mercy.edu/about-mercy-college/work-at-mercy/benefits-compensation/',
        'vacation': [(1,15)],
        'sick_days': 12,
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.mercy.edu',
    'jobs_page_url': 'https://jobs.mercy.edu/applicants/jsp/shared/Welcome_css.jsp',

    'empcnt': [501,1000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
