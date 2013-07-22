from neekanee.jobscrapers.peopleadmin.PeopleAdminATS import PeopleAdminJobScraper

COMPANY = {
    'name': 'Universiy of Kansas',
    'hq': 'Lawrence, KS',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.ku.edu',
    'jobs_page_url': 'https://jobs.ku.edu/applicants/jsp/shared/Welcome_css.jsp',

    'empcnt': [10001]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
