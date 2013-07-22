from neekanee.jobscrapers.peopleadmin.peopleadmin2 import PeopleAdminJobScraper

COMPANY = {
    'name': 'University of Central Oklahoma',
    'hq': 'Edmond, OK',

    'benefits': {
        'url': 'http://www.uco.edu/administration/human-resources/benefits/index.asp',
        'vacation': [(1,15),(4,16),(5,17),(6,18),(7,19),(8,20),(11,21),(16,22)],
        'holidays': 12,
        'sick_days': 15
    },

    'home_page_url': 'http://www.uco.edu',
    'jobs_page_url': 'https://jobs.uco.edu/applicants/jsp/shared/index.jsp',

    'empcnt': [1001,5000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
