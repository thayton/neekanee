from neekanee.jobscrapers.peopleadmin.PeopleAdminATS import PeopleAdminJobScraper

COMPANY = {
    'name': 'Oregon State University',
    'hq': 'Corvallis, OR',

    'benefits': {
        'url': 'http://oregonstate.edu/admin/hr/jobs/benefits.html',
        'vacation': [(1,22)],
        'holidays': 8,
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.oregonstate.edu',
    'jobs_page_url': 'https://jobs.oregonstate.edu/applicants/jsp/shared/Welcome_css.jsp',

    'empcnt': [1001,5000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
