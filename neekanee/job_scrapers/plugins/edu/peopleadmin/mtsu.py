from neekanee.jobscrapers.peopleadmin.PeopleAdminATS import PeopleAdminJobScraper

COMPANY = {
    'name': 'Middle Tennessee State University',
    'hq': 'Murfreesboro, TN',

    'home_page_url': 'http://www.mtsu.edu',
    'jobs_page_url': 'https://mtsujobs.mtsu.edu/applicants/jsp/shared/Welcome_css.jsp',

    'empcnt': [1001,5000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
