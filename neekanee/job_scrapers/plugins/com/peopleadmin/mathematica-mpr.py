from neekanee.jobscrapers.peopleadmin.peopleadmin2 import PeopleAdminJobScraper

COMPANY = {
    'name': 'Mathematica Policy Research',
    'hq': 'Cambridge, MA',

    'ats': 'PeopleAdmin',

    'home_page_url': 'http://www.mathematica-mpr.com',
    'jobs_page_url': 'https://careers.mathematica-mpr.com/applicants/jsp/shared/index.jsp',

    'empcnt': [501,1000]
}

class MathematicaMprJobScraper(PeopleAdminJobScraper):
    def __init__(self):
        super(MathematicaMprJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        l = td[3].contents[0]
        return self.parse_location(td[3].contents[0])
        
def get_scraper():
    return MathematicaMprJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
