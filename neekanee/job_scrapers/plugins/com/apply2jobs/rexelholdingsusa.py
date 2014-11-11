from neekanee.jobscrapers.apply2jobs.apply2jobs import Apply2JobsJobScraper
from neekanee_solr.models import *

COMPANY = {
    'name': 'Rexel Holdings USA',
    'hq': 'Dallas, TX',

    'home_page_url': 'http://www.rexelholdingsusa.com',
    'jobs_page_url': 'https://www1.apply2jobs.com/RexelHoldings/ProfExt/?fuseaction=mExternal.showSearchInterface',

    'empcnt': [5001, 10000]
}

class RexelJobScraper(Apply2JobsJobScraper):
    def __init__(self):
        super(RexelJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        l = td[3].text + ',' + td[4].text
        return self.parse_location(l)

def get_scraper():
    return RexelJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
