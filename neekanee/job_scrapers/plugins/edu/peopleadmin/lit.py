from neekanee.jobscrapers.peopleadmin.PeopleAdminATS import PeopleAdminJobScraper

COMPANY = {
    'name': 'Lamar Institute of Technology',
    'hq': 'Beaumont,TX',

    'benefits': {
        'url': 'http://dept.lamar.edu//humanresources/hr_EmpBenefits.php',
        'vacation': []
    },

    'home_page_url': 'http://www.lit.edu',
    'jobs_page_url': 'https://jobs.lit.edu/applicants/jsp/shared/Welcome_css.jsp',

    'empcnt': [51,200]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)
