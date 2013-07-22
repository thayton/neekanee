from neekanee.jobscrapers.peopleadmin.peopleadmin2 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Wake Technical Community College',
    'hq': 'Raleigh, NC',

    'home_page_url': 'http://www.waketech.edu',
    'jobs_page_url': 'https://jobs.waketech.edu/applicants/jsp/shared/index.jsp',

    'gctw_chronicle': True,

    'empcnt': [501,1000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
