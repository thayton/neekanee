from neekanee.jobscrapers.peopleadmin.peopleadmin3 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Howard Community College',
    'hq': 'Columbia, MD',

    'benefits': {
        'url': 'http://www.howardcc.edu/Visitors/HR/Benefits/Benefits.html',
        'vacation': [(1,20)],
        'holidays': 17,
        'sick_days': 12,
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.howardcc.edu',
    'jobs_page_url': 'https://www.hccjobs.org',

    'gctw_chronicle': True,

    'empcnt': [501,1000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
