from neekanee.jobscrapers.peopleadmin.PeopleAdminATS import PeopleAdminJobScraper

COMPANY = {
    'name': 'University of Rhode Island',
    'hq': 'Kingston, RI',

    'home_page_url': 'http://www.uri.edu',
    'jobs_page_url': 'https://jobs.uri.edu/applicants/jsp/shared/Welcome_css.jsp',

    'empcnt': [1001,5000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
