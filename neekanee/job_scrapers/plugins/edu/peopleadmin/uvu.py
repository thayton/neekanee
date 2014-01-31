from neekanee.jobscrapers.peopleadmin.peopleadmin3 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Utah Valley University',
    'hq': 'Orem, UT',

    'home_page_url': 'http://www.uvu.edu',
    'jobs_page_url': 'https://www.uvu.jobs',

    'empcnt': [1001,5000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
