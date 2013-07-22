from neekanee.jobscrapers.peopleadmin.peopleadmin2 import PeopleAdminJobScraper

COMPANY = {
    'name': 'University of California, Santa Barbara',
    'hq': 'Santa Barbara, CA',

    'home_page_url': 'http://www.ucsb.edu',
    'jobs_page_url': 'https://jobs.ucsb.edu/applicants/jsp/shared/index.jsp',

    'empcnt': [5001,10000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
