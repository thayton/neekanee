from neekanee.jobscrapers.apply2jobs.apply2jobs import Apply2JobsJobScraper

COMPANY = {
    'name': 'REI',
    'hq': 'Sumner, WA',

    'home_page_url': 'http://www.rei.com',
    'jobs_page_url': 'https://www.rei.apply2jobs.com/ProfExt/index.cfm?fuseaction=mExternal.showSearchInterface',

    'empcnt': [5001,10000]
}

class ReiJobScraper(Apply2JobsJobScraper):
    def __init__(self):
        super(ReiJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[3].text + ',' + td[4].text)

def get_scraper():
    return ReiJobScraper()
