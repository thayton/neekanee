from neekanee.jobscrapers.peopleadmin.peopleadmin3 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Shippensburg University',
    'hq': 'Shippensburg, PA',

    'home_page_url': 'http://www.ship.edu',
    'jobs_page_url': 'https://jobs.ship.edu/',

    'empcnt': [201,500]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
