from neekanee.jobscrapers.peopleadmin.peopleadmin3 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Gettysburg College',
    'hq': 'Gettysburg, PA',

    'benefits': {
        'url': 'http://www.gettysburg.edu/about/offices/president/hr/benefits/',
        'vacation': [],
        'holidays': 10,
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.gettysburg.edu',
    'jobs_page_url': 'https://gettysburg.peopleadmin.com',

    'gctw_chronicle': True,

    'empcnt': [501,1000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
        
