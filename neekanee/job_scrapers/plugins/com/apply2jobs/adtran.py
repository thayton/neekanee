from neekanee.jobscrapers.apply2jobs.apply2jobs import Apply2JobsJobScraper
from neekanee_solr.models import *

COMPANY = {
    'name': 'ADTRAN',
    'hq': 'Huntsville, AL',

    'home_page_url': 'http://www.adtran.com',
    'jobs_page_url': 'https://www1.apply2jobs.com/ADTRAN/ProfExt/index.cfm?fuseaction=mExternal.showSearchInterface',

    'empcnt': [1001, 5000]
}

class AdtranJobScraper(Apply2JobsJobScraper):
    def __init__(self):
        super(AdtranJobScraper, self).__init__(COMPANY)

    def update_frmSearch_form(self):
        self.br.form.set_value_by_label(['United States'], name='searchCountryID')

    def get_location_from_td(self, td):
        l = td[3].text + ',' + td[4].text
        return self.parse_location(l)

def get_scraper():
    return AdtranJobScraper()
