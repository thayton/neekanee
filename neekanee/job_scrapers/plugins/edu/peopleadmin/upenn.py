from neekanee.jobscrapers.peopleadmin.peopleadmin3 import PeopleAdminJobScraper

COMPANY = {
    'name': 'University of Pennsylvania',
    'hq': 'Philadelphia, PA',

    'home_page_url': 'http://www.upenn.edu/',
    'jobs_page_url': 'https://jobs.hr.upenn.edu',

    'empcnt': [10001]
}

class UpennStateJobScraper(PeopleAdminJobScraper):
    def __init__(self):
        super(UpennStateJobScraper, self).__init__(COMPANY)

def get_scraper():
    return UpennStateJobScraper()

if __name__:
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
