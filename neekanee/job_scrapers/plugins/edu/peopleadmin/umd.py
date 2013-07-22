from neekanee.jobscrapers.peopleadmin.PeopleAdminATS import PeopleAdminJobScraper

COMPANY = {
    'name': 'University of Maryland',
    'hq': 'College Park, MD',

    'benefits': {
        'url': 'http://www.uhr.umd.edu/benefits/',
        'vacation': [(1,22),(21,25)],
        'holidays': 17,
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.umd.edu',
    'jobs_page_url': 'https://jobs.umd.edu/applicants/jsp/shared/Welcome_css.jsp',

    'empcnt': [10001]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
