from neekanee.jobscrapers.peopleadmin.peopleadmin3 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Wellesley College',
    'hq': 'Wellesley, MA',

    'home_page_url': 'http://www.wellesley.edu',
    'jobs_page_url': 'https://career.wellesley.edu',

    'empcnt': [501,1000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
