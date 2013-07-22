from neekanee.jobscrapers.peopleadmin.peopleadmin3 import PeopleAdminJobScraper

COMPANY = {
    'name': 'George Washington University',
    'hq': 'Washington, DC',

    'benefits': {
        'url': 'http://www.gwu.edu/employment/careersatgw/benefits',
        'vacation': [(1,15),(3,18),(5,21),(16,24)],
        'tuition_assistance': True
    },

    'home_page_url': 'http://www.gwu.edu',
    'jobs_page_url': 'https://www.gwu.jobs',

    'empcnt': [5001,10000]
}

class GwuJobScraper(PeopleAdminJobScraper):
    def __init__(self):
        super(GwuJobScraper, self).__init__(COMPANY)

    def location_handler(self, l):
        locations = { 'Foggy Bottom': 'Washington, DC',
                      'Ashburn':      'Ashburn, VA',
                      'Alexandria':   'Alexandria, VA',
                      'Arlington':    'Arlington, VA',
                      'Hampton':      'Hampton, VA',
                      'Mount Vernon': 'Washington, DC',
                      'Rockville':    'Rockville, MD' }

        for p in locations.keys():
            if l == p:
                return self.parse_location(locations[p])

def get_scraper():
    return GwuJobScraper()
