from neekanee.jobscrapers.peopleadmin.peopleadmin3 import PeopleAdminJobScraper

COMPANY = {
    'name': 'University of Nebraska - Lincoln',
    'hq': 'Lincoln, NE',

    'home_page_url': 'http://www.unl.edu',
    'jobs_page_url': 'https://employment.unl.edu',

    'empcnt': [1001,5000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
