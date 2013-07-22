from neekanee.jobscrapers.peopleadmin.peopleadmin3 import PeopleAdminJobScraper


COMPANY = {
    'name': 'Missouri State University-West Plains',
    'hq': 'West Plains, MO',

    'home_page_url': 'http://wp.missouristate.edu',
    'jobs_page_url': 'http://wp.missouristate.edu/employmentopportunities/',

    'gctw_chronicle': True,

    'empcnt': [51,200]
}

def get_scraper():
    job_scraper = PeopleAdminJobScraper(COMPANY)
    job_scraper.link_text = 'Search Jobs'
    return job_scraper

