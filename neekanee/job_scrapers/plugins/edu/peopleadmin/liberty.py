from neekanee.jobscrapers.peopleadmin.PeopleAdminATS import PeopleAdminJobScraper

COMPANY = {
    'name': 'Liberty University',
    'hq': 'Lynchburg, VA',

    'benefits': {
        'url': 'http://www.liberty.edu/index.cfm?PID=731',
        'vacation': [(1,10),
                     (5,11),
                     (6,12),
                     (7,13),
                     (8,14),
                     (9,15),
                     (10,16),
                     (11,17),
                     (12,18),
                     (13,19),
                     (14,20)],
        'sick_days': 5,
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.liberty.edu',
    'jobs_page_url': 'https://jobs.liberty.edu/applicants/jsp/shared/Welcome_css.jsp',

    'empcnt': [1001,5000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
