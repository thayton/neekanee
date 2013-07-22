from neekanee.jobscrapers.peopleadmin.peopleadmin2 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Auburn University',
    'hq': 'Auburn, AL',

    'home_page_url': 'http://www.auburn.edu',
    'jobs_page_url': 'https://www.auemployment.com/applicants/jsp/shared/index.jsp',

    'empcnt': [5001,10000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
