from neekanee.jobscrapers.peopleadmin.PeopleAdminATS import PeopleAdminJobScraper

COMPANY = {
    'name': 'Nicholls State University',
    'hq': 'Thibodaux, Louisiana',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.nicholls.edu',
    'jobs_page_url': 'https://jobs.nicholls.edu/applicants/jsp/shared/Welcome_css.jsp',

    'empcnt': [201,500]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
