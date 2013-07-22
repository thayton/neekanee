from neekanee.jobscrapers.peopleadmin.PeopleAdminATS import PeopleAdminJobScraper

COMPANY = {
    'name': 'College of Lake County',
    'hq': 'Grayslake, IL',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.clcillinois.edu',
    'jobs_page_url': 'https://jobs.clcillinois.edu/applicants/jsp/shared/Welcome_css.jsp',

    'empcnt': [1001,5000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
