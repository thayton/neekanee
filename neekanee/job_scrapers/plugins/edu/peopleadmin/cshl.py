from neekanee.jobscrapers.peopleadmin.peopleadmin3 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Cold Spring Harbor Laboratory ',
    'hq': 'Cold Spring Harbor, NY',

    'home_page_url': 'http://www.cshl.edu',
    'jobs_page_url': 'https://cshl.peopleadmin.com/postings/search',

    'empcnt': [1001,5000]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
