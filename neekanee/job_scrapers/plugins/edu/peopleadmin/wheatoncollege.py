from neekanee.jobscrapers.peopleadmin.peopleadmin3 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Wheaton College',
    'hq': 'Norton, MA',

    'home_page_url': 'http://www.wheatoncollege.edu',
    'jobs_page_url': 'https://jobs.wheatoncollege.edu',

    'empcnt': [201,500]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
