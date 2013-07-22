from neekanee.jobscrapers.peopleadmin.peopleadmin3 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Jacksonville State University',
    'hq': 'Jacksonville, AL',

    'benefits': {
        'url': 'http://www.jsu.edu/hr/benefits_summary.html',
        'vacation': [(1,12),(10,15),(20,18)],
        'holidays': 19,
        'sick_days': 12,
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.jsu.edu',
    'jobs_page_url': 'https://jobs.jsu.edu',

    'gctw_chronicle': True,

    'empcnt': [1001,5000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
