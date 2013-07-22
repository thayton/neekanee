from neekanee.jobscrapers.peopleadmin.peopleadmin3 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Washington and Lee University',
    'hq': 'Lexington, VA',

    'home_page_url': 'http://www.wlu.edu',
    'jobs_page_url': 'https://jobs.wlu.edu',

    'gctw_chronicle': True,

    'empcnt': [501,1000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
