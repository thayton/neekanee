from neekanee.jobscrapers.peopleadmin.peopleadmin2 import PeopleAdminJobScraper

COMPANY = {
    'name': 'University of North Texas',
    'hq': 'Denton, TX',

    'home_page_url': 'http://www.unt.edu',
    'jobs_page_url': 'https://jobs.unt.edu/applicants/jsp/shared/index.jsp',

    'empcnt': [1001,5000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
