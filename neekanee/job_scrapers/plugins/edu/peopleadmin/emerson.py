from neekanee.jobscrapers.peopleadmin.peopleadmin3 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Emerson College',
    'hq': 'Boston, MA',

    'home_page_url': 'http://www.emerson.edu',
    'jobs_page_url': 'https://emerson.peopleadmin.com/postings/search',

    'empcnt': [201,500]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
