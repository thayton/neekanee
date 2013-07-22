from neekanee.jobscrapers.apply2jobs.apply2jobs import Apply2JobsJobScraper

COMPANY = {
    'name': 'Cisco',
    'hq': 'San Jose, CA',

    'home_page_url': 'http://www.cisco.com',
    'jobs_page_url': 'https://www.cisco.apply2jobs.com/ProfExt/index.cfm?fuseaction=mExternal.showSearchInterface',

    'empcnt': [10001]
}

class CiscoJobScraper(Apply2JobsJobScraper):
    def __init__(self):
        super(CiscoJobScraper, self).__init__(COMPANY)
        self.geocoder.return_usa_only = False

    def update_frmSearch_form(self):
        self.br.form['searchAuxCountryID'] = ['228', '44', '102'] # United States, China, and India

    def get_location_from_td(self, td):
        return self.parse_location(td[2].text)

def get_scraper():
    return CiscoJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
