from neekanee.jobscrapers.peopleadmin.peopleadmin2 import PeopleAdminJobScraper

COMPANY = {
    'name': 'City College of San Francisco',
    'hq': 'San Francisco, CA',

    'home_page_url': 'http://www.ccsf.edu',
    'jobs_page_url': 'https://jobs.ccsf.edu/applicants/jsp/shared/index.jsp',

    'empcnt': [1001,5000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
