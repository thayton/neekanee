from neekanee.jobscrapers.peopleadmin.PeopleAdminATS import PeopleAdminJobScraper

COMPANY = {
    'name': 'University of West Georgia',
    'hq': 'Carrollton, GA',

    'home_page_url': 'http://www.westga.edu',
    'jobs_page_url': 'https://jobs.westga.edu/applicants/jsp/shared/Welcome_css.jsp',

    'empcnt': [501,1000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
