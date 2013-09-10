from neekanee.jobscrapers.peopleadmin.peopleadmin3 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Furman University',
    'hq': 'Greenville, SC',

    'home_page_url': 'http://www.furman.edu',
    'jobs_page_url': 'https://jobs.furman.edu/',

    'empcnt': [501,1000]
}

class FurmanJobScraper(PeopleAdminJobScraper):
    def __init__(self):
        super(FurmanJobScraper, self).__init__(COMPANY)

def get_scraper():
    return FurmanJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
