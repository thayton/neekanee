from neekanee.jobscrapers.peopleadmin.peopleadmin3 import PeopleAdminJobScraper

COMPANY = {
    'name': 'University of Mississippi',
    'hq': 'University, MS',

    'benefits': {
        'url': 'http://www.olemiss.edu/depts/hr/benefits.html',
        'vacation': [(1,18),(4,21),(9,24),(16,27)],
        'holidays': 8,
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.olemiss.edu',
    'jobs_page_url': 'https://jobs.olemiss.edu',

    'gctw_chronicle': True,

    'empcnt': [10001]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
