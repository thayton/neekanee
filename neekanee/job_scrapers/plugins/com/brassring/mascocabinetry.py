from neekanee.jobscrapers.brassring.brassring import BrassringJobScraper
from neekanee.htmlparse.soupify import soupify

COMPANY = {
    'name': 'Masco Cabinetry',
    'hq': 'Ann Arbor, MI',

    'home_page_url': 'http://www.mascocabinetry.com',
    'jobs_page_url': 'https://sjobs.brassring.com/TGWebHost/home.aspx?partnerid=25204&siteid=5219',

    'empcnt': [1001,5000]
}

class MascoCabinetryJobScraper(BrassringJobScraper):
    def __init__(self):
        super(MascoCabinetryJobScraper, self).__init__(COMPANY)
        self.soupify_search_form = True

    def get_url_from_formtext(self, x):
        s = soupify(x['AutoReq'])
        return s.a

    def get_title_from_formtext(self, x):
        return x['JobTitle']

    def get_location_from_formtext(self, x):
        l = x['FORMTEXT1'] + ', ' + x['FORMTEXT5'] + ', ' + x['FORMTEXT4']
        l = self.parse_location(l)

        return l
    
def get_scraper():
    return MascoCabinetryJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
