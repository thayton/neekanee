from neekanee.jobscrapers.peopleadmin.peopleadmin3 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Mt. San Antonio College',
    'hq': 'Walnut, CA',

    'home_page_url': 'http://www.mtsac.edu',
    'jobs_page_url': 'https://hrjobs.mtsac.edu',

    'empcnt': [1001,5000]
}

class MtsacJobScraper(PeopleAdminJobScraper):
    def __init__(self):
        super(MtsacJobScraper, self).__init__(COMPANY)

def get_scraper():
    return MtsacJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
