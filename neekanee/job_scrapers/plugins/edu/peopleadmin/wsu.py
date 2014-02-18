from neekanee.jobscrapers.peopleadmin.peopleadmin3 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Washington State University',
    'hq': 'Pullman, WA',

    'home_page_url': 'http://www.wsu.edu',
    'jobs_page_url': 'https://www.wsujobs.com',

    'empcnt': [1001,5000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
