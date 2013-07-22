from neekanee.jobscrapers.peopleadmin.peopleadmin2 import PeopleAdminJobScraper

COMPANY = {
    'name': 'University of Virginia',
    'hq': 'Charlottesville, VA',

    'home_page_url': 'http://www.virginia.edu',
    'jobs_page_url': 'https://jobs.virginia.edu/applicants/jsp/shared/index.jsp',

    'empcnt': [10001]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
