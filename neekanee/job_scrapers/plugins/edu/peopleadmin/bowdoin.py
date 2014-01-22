from neekanee.jobscrapers.peopleadmin.peopleadmin2 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Bowdoin College',
    'hq': 'Portland, Maine',

    'home_page_url': 'http://www.bowdoin.edu',
    'jobs_page_url': 'https://careers.bowdoin.edu/applicants/jsp/shared/index.jsp',

    'empcnt': [201,500]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
