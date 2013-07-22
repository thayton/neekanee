from neekanee.jobscrapers.peopleadmin.peopleadmin2 import PeopleAdminJobScraper

COMPANY = {
    'name': 'University of Southern California',
    'hq': 'Los Angeles, CA',

    'home_page_url': 'http://www.usc.edu',
    'jobs_page_url': 'https://jobs.usc.edu/applicants/jsp/shared/index.jsp',

    'gctw_chronicle': True,

    'empcnt': [10001]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
