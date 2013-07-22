from neekanee.jobscrapers.peopleadmin.peopleadmin2 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Florida Atlantic University',
    'hq': 'Boca Raton, FL',

    'benefits': {
        'url': 'http://www.fau.edu/hr/Benefits/index.php',
        'vacation': []
    },

    'home_page_url': 'http://www.fau.edu',
    'jobs_page_url': 'https://jobs.fau.edu/applicants/jsp/shared/index.jsp',

    'empcnt': [1001,5000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
