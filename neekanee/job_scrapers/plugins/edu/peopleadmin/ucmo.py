from neekanee.jobscrapers.peopleadmin.peopleadmin3 import PeopleAdminJobScraper

COMPANY = {
    'name': 'University of Central Missouri',
    'hq': 'Warrensburg, MO',

    'home_page_url': 'http://www.ucmo.edu',
    'jobs_page_url': 'https://jobs.ucmo.edu',
    
    'empcnt': [1001,5000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
