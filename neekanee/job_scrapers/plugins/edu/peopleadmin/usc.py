from neekanee.jobscrapers.peopleadmin.peopleadmin3 import PeopleAdminJobScraper

COMPANY = {
    'name': 'University of Southern California',
    'hq': 'Los Angeles, CA',

    'home_page_url': 'http://www.usc.edu',
    'jobs_page_url': 'https://jobs.usc.edu',

    'empcnt': [10001]
}

def get_scraper():
    return PeopleAdminJobScraper(COMPANY)

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
