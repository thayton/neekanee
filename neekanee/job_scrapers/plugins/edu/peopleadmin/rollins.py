from neekanee.jobscrapers.peopleadmin.peopleadmin3 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Rollins College',
    'hq': 'Winter Park, FL',

    'home_page_url': 'http://www.rollins.edu',
    'jobs_page_url': 'https://www.rollinsjobs.com',

    'empcnt': [501,1000]
}

def get_scraper():
    job_scraper = PeopleAdminJobScraper(COMPANY)
    job_scraper.link_text = 'Search Openings'
    return job_scraper
