from neekanee.jobscrapers.peopleadmin.PeopleAdminATS import PeopleAdminJobScraper

COMPANY = {
    'name': 'Mount Holyoke College',
    'hq': 'South Hadley, MA',

    'benefits': {
        'url': 'http://www.mtholyoke.edu/hr/benefits.html',
        'vacation': [],
        'holidays': 12,
        'sick_days': 15,
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.mtholyoke.edu',
    'jobs_page_url': 'https://jobsearch.mtholyoke.edu/applicants/jsp/shared/Welcome_css.jsp',

    'empcnt': [501,1000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
