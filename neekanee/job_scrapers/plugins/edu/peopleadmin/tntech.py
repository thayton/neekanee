from neekanee.jobscrapers.peopleadmin.PeopleAdminATS import PeopleAdminJobScraper

COMPANY = {
    'name': 'Tennessee Tech University',
    'hq': 'Cookeville, TN',

    'benefits': {
        'url': 'http://www.tntech.edu/hr/benefits/',
        'vacation': [],
        'holidays': 13
    },

    'home_page_url': 'http://www.tntech.edu',
    'jobs_page_url': 'https://jobs.tntech.edu/applicants/jsp/shared/Welcome_css.jsp',

    'empcnt': [1001,5000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
