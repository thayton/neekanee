from neekanee.jobscrapers.peopleadmin.peopleadmin2 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Columbia University',
    'hq': 'New York, NY',

    'home_page_url': 'http://www.columbia.edu',
    'jobs_page_url': 'https://jobs.columbia.edu/applicants/jsp/shared/index.jsp',

    'empcnt': [10001]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
