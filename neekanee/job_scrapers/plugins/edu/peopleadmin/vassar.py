from neekanee.jobscrapers.peopleadmin.peopleadmin2 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Vassar College',
    'hq': 'Poughkeepsie, NY',

    'home_page_url': 'http://www.vassar.edu',
    'jobs_page_url': 'https://employment.vassar.edu/applicants/jsp/shared/index.jsp',

    'empcnt': [201,500]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
