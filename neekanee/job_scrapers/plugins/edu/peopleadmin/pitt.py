from neekanee.jobscrapers.peopleadmin.peopleadmin3 import PeopleAdminJobScraper

COMPANY = {
    'name': 'University of Pittsburgh',
    'hq': 'Pittsburgh, PA',

    'home_page_url': 'http://www.pitt.edu',
    'jobs_page_url': 'https://www.pittsource.com/postings/search',

    'empcnt': [10001]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
