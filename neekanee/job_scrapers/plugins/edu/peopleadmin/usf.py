from neekanee.jobscrapers.peopleadmin.PeopleAdminATS import PeopleAdminJobScraper

COMPANY = {
    'name': 'University of South Florida',
    'hq': 'Tampa, FL',

    'home_page_url': 'http://www.usf.edu',
    'jobs_page_url': 'https://employment.usf.edu/applicants/jsp/shared/Welcome_css.jsp',

    'empcnt': [5001,10000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
