from neekanee.jobscrapers.peopleadmin.peopleadmin3 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Virginia Tech',
    'hq': 'Blacksburg, VA',

    'home_page_url': 'http://www.vt.edu',
    'jobs_page_url': 'https://listings.jobs.vt.edu/',

    'empcnt': [5001,10000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
