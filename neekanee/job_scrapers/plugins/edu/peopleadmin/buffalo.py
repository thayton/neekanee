from neekanee.jobscrapers.peopleadmin.PeopleAdminATS import PeopleAdminJobScraper

COMPANY = {
    'name': 'State University of New York at Buffalo',
    'hq': 'Buffalo, NY',

    'benefits': {
        'url': 'http://hr.buffalo.edu/index.php?module=pagemaster&PAGE_user_op=view_page&PAGE_id=3&MMN_position=442:440:441',
        'vacation': []
    },

    'home_page_url': 'http://www.buffalo.edu',
    'jobs_page_url': 'https://www.ubjobs.buffalo.edu/applicants/jsp/shared/Welcome_css.jsp',

    'gctw_chronicle': True,

    'empcnt': [5001,10000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
