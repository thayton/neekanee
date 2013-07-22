from neekanee.jobscrapers.peopleadmin.PeopleAdminATS import PeopleAdminJobScraper

COMPANY = {
    'name': 'Kansas University Medical Center',
    'hq': 'Kansas City, KS',

    'benefits': {
        'url': 'http://www2.kumc.edu/hr/benefits/benefits.html',
        'vacation': [],
        'holidays': 10,
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.kumc.edu',
    'jobs_page_url': 'https://pa124.peopleadmin.com/applicants/jsp/shared/Welcome_css.jsp',

    'empcnt': [1001,5000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
