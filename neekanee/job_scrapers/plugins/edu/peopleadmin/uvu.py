from neekanee.jobscrapers.peopleadmin.peopleadmin2 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Utah Valley University',
    'hq': 'Orem, UT',

    'home_page_url': 'http://www.uvu.edu',
    'jobs_page_url': 'https://www.uvu.jobs/applicants/jsp/shared/index.jsp',

    'empcnt': [1001,5000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
