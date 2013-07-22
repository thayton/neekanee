from neekanee.jobscrapers.peopleadmin.PeopleAdminATS import PeopleAdminJobScraper

COMPANY = {
    'name': 'College of the Redwoods',
    'hq': 'Eureka, CA',

    'benefits': {
        'url': 'http://www.redwoods.edu/humanresources/benefits.asp',
        'vacation': []
    },

    'home_page_url': 'http://www.redwoods.edu',
    'jobs_page_url': 'https://employment.redwoods.edu/applicants/jsp/shared/Welcome_css.jsp',

    'empcnt': [201,500]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
