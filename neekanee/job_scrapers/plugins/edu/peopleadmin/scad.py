from neekanee.jobscrapers.peopleadmin.peopleadmin3 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Savannah College of Art and Design',
    'hq': 'Savannah, GA',

    'home_page_url': 'http://www.scad.edu',
    'jobs_page_url': 'https://scadjobs.scad.edu',

    'empcnt': [51,200]
}

class ScadJobScraper(PeopleAdminJobScraper):
    def __init__(self):
        super(ScadJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[2].text)

def get_scraper():
    return ScadJobScraper()

if __name__:
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
