from neekanee.jobscrapers.brassring.brassring import BrassringJobScraper
from neekanee.htmlparse.soupify import soupify

COMPANY = {
    'name': 'Diageo',
    'hq': 'London, United Kingdom',

    'home_page_url': 'http://www.diageo.com',
    'jobs_page_url': 'http://jobs.brassring.com/TGWebHost/home.aspx?partnerid=11729&siteid=208',

    'empcnt': [10001]
}

class DiageoJobScraper(BrassringJobScraper):
    def __init__(self):
        super(DiageoJobScraper, self).__init__(COMPANY)
        self.soupify_search_form = True

    def get_url_from_formtext(self, x):
        s = soupify(x['FormText10'])
        return s.a

    def get_title_from_formtext(self, x):
        s = soupify(x['FormText10'])
        return s.a.text

    def get_location_from_formtext(self, x):
        l = x['FORMTEXT14'] + ', ' + x['FormText12']
        l = self.parse_location(l)

        return l

def get_scraper():
    return DiageoJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
