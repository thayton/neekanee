from neekanee.jobscrapers.peopleadmin.PeopleAdminATS import PeopleAdminJobScraper

COMPANY = {
    'name': 'Washington State University',
    'hq': 'Pullman, WA',

    'home_page_url': 'http://www.wsu.edu',
    'jobs_page_url': 'https://www.wsujobs.com/applicants/jsp/shared/Welcome_css.jsp',

    'empcnt': [1001,5000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
