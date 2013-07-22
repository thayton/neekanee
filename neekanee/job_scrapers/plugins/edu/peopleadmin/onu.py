from neekanee.jobscrapers.peopleadmin.peopleadmin3 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Ohio Northern University',
    'hq': 'Ada, Ohio',

    'benefits': {
        'url': 'http://www.onu.edu/administration/human_resources/benefits',
        'vacation': [],
        'holidays': 16,
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.onu.edu',
    'jobs_page_url': 'https://jobs.onu.edu',

    'empcnt': [201,500]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
