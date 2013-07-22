from neekanee.jobscrapers.peopleadmin.PeopleAdminATS import PeopleAdminJobScraper

COMPANY = {
    'name': 'University of Chicago',
    'hq': 'Chicago, IL',

    'benefits': {
        'url': 'http://hrservices.uchicago.edu/benefits/',
        'vacation': [(1,15),(9,20),(21,25)],
        'holidays': 8,
        'sick_days': 18,
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.uchicago.edu',
    'jobs_page_url': 'https://jobopportunities.uchicago.edu/applicants/jsp/shared/Welcome_css.jsp',

    'empcnt': [5001,10000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
