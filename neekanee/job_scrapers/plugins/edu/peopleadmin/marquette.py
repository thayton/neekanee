from neekanee.jobscrapers.peopleadmin.peopleadmin3 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Marquette University',
    'hq': 'Milwaukee, WI',

    'home_page_url': 'http://www.marquette.edu',
    'jobs_page_url': 'https://employment.marquette.edu',

    'empcnt': [1001,5000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
