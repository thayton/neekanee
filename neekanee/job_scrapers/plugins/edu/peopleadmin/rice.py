from neekanee.jobscrapers.peopleadmin.PeopleAdminATS import PeopleAdminJobScraper

COMPANY = {
    'name': 'Rice University',
    'hq': 'Houston, TX',

    'benefits': {
        'url': 'http://cohesion.rice.edu/campusservices/humanresources/riceworks.cfm?doc_id=12961',
        'vacation': [(1,21),(11,26)],
        'holidays': 12
    },

    'home_page_url': 'http://www.rice.edu',
    'jobs_page_url': 'https://jobs.rice.edu/applicants/jsp/shared/Welcome_css.jsp',

    'gctw_chronicle': True,

    'empcnt': [1001,5000]
}

def get_scraper():
    job_scraper = PeopleAdminJobScraper(COMPANY)
    job_scraper.link_text = 'Search Current Jobs'
    return job_scraper
