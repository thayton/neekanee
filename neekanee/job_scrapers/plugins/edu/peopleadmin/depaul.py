from neekanee.jobscrapers.peopleadmin.PeopleAdminATS import PeopleAdminJobScraper

COMPANY = {
    'name': 'DePaul University',
    'hq': 'Chicago, IL',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.depaul.edu',
    'jobs_page_url': 'https://facultyopportunities.depaul.edu/applicants/jsp/shared/Welcome_css.jsp',

    'empcnt': [1001,5000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
