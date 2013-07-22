from neekanee.jobscrapers.peopleadmin.PeopleAdminATS import PeopleAdminJobScraper

COMPANY = {
    'name': 'Princeton University',
    'hq': 'Princeton, NJ',

    'benefits': {
        'url': 'http://www.princeton.edu/hr/benefits/',
        'vacation': [],
        'holidays': 9,
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.princeton.edu',
    'jobs_page_url': 'https://jobs.princeton.edu/applicants/jsp/shared/Welcome_css.jsp',

    'empcnt': [5001,10000]
}

def get_scraper():
    job_scraper = PeopleAdminJobScraper(COMPANY)
    job_scraper.link_text = 'Search Open Positions'
    return job_scraper
