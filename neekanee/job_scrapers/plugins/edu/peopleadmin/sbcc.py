from neekanee.jobscrapers.peopleadmin.peopleadmin3 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Santa Barbara City College',
    'hq': 'Santa Barbara, CA',

    'home_page_url': 'http://www.sbcc.edu',
    'jobs_page_url': 'https://jobs.sbcc.edu/',

    'empcnt': [1001,5000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
