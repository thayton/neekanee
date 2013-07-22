from neekanee.jobscrapers.peopleadmin.PeopleAdminATS import PeopleAdminJobScraper

COMPANY = {
    'name': 'Columbus State Community College',
    'hq': 'Columbus, OH',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.cscc.edu',
    'jobs_page_url': 'https://jobs.cscc.edu/applicants/jsp/shared/Welcome_css.jsp',

    'empcnt': [501,1000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
