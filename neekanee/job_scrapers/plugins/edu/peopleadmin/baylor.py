from neekanee.jobscrapers.peopleadmin.PeopleAdminATS import PeopleAdminJobScraper

COMPANY = {
    'name': 'Baylor University',
    'hq': 'Waco, TX',

    'benefits': {
        'url': 'http://www.baylor.edu/hr/index.php?id=80786',
        'vacation': [],
        'holidays': 15,
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.baylor.edu',
    'jobs_page_url': 'https://jobs.baylor.edu/applicants/jsp/shared/Welcome_css.jsp',

    'empcnt': [1001,5000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
