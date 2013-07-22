from neekanee.jobscrapers.peopleadmin.peopleadmin2 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Shepherd University',
    'hq': 'Shepherdstown, WV',

    'benefits': {
        'url': 'http://www.shepherd.edu/hrweb/policies1.html',
        'vacation': [(1,24)],
        'holidays': 14,
        'sick_leave': 18
    },

    'home_page_url': 'http://www.shepherd.edu',
    'jobs_page_url': 'https://jobs.shepherd.edu/applicants/jsp/shared/index.jsp',

    'empcnt': [201,500]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
