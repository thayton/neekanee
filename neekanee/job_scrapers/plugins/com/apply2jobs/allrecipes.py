from neekanee.jobscrapers.apply2jobs.apply2jobs import Apply2JobsJobScraper
from neekanee_solr.models import *

COMPANY = {
    'name': 'All Recipes',
    'hq': 'Seattle, WA',

    'home_page_url': 'http://allrecipes.com',
    'jobs_page_url': 'https://www.meredith.apply2jobs.com/ProfExt/index.cfm?fuseaction=mExternal.showSearchInterface',

    'empcnt': [51,200]
}

class AllRecipesJobScraper(Apply2JobsJobScraper):
    def __init__(self):
        super(AllRecipesJobScraper, self).__init__(COMPANY)

    def update_frmSearch_form(self):
        self.br.form['txtKeyword'] = 'allrecipes.com'

    def get_location_from_td(self, td):
        l = td[1].text + ',' + td[2].text
        return self.parse_location(l)


def get_scraper():
    return AllRecipesJobScraper()
