from neekanee.jobscrapers.peopleadmin.PeopleAdminATS import PeopleAdminJobScraper

COMPANY = {
    'name': 'Texas A&M University',
    'hq': 'San Antonio, TX',

    'benefits': {
        'url': 'http://employees.tamu.edu/employees/benefits/',
        'vacation': [(1,12),(3,13.5),(6,15),(11,16.5),(16,19.5),(21,22.5),(26,25.5),(31,28.5),(36,31.5)],
        'holidays': 15,
        'sick_days': 12
    },

    'home_page_url': 'http://www.tamu.edu',
    'jobs_page_url': 'https://employment.tamusahr.com/applicants/jsp/shared/Welcome_css.jsp',

    'empcnt': [10001]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
