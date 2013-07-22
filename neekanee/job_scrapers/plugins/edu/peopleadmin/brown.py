from neekanee.jobscrapers.peopleadmin.peopleadmin2 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Brown University',
    'hq': 'Providence, ri',

    'benefits': {'vacation': []},

    'home_page_url': 'http://www.brown.edu',
    'jobs_page_url': 'https://careers.brown.edu/applicants/jsp/shared/index.jsp',

    'empcnt': [1001,5000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
