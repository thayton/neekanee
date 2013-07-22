from neekanee.jobscrapers.peopleadmin.peopleadmin2 import PeopleAdminJobScraper

COMPANY = {
    'name': 'State University of New York at Fredonia',
    'hq': 'Fredonia, NY',

    'benefits': {
        'url': 'http://www.fredonia.edu/humanresources/benefits.asp',
        'vacation': []
    },

    'home_page_url': 'http://www.fredonia.edu',
    'jobs_page_url': 'https://careers.fredonia.edu/applicants/jsp/shared/index.jsp',

    'gctw_chronicle': True,

    'empcnt': [501,1000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
