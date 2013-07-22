from neekanee.jobscrapers.brassring.brassring import BrassringJobScraper
from neekanee.htmlparse.soupify import soupify

COMPANY = {
    'name': 'Turner',
    'hq': 'Atlanta, GA',

    'home_page_url': 'http://www.turner.com',
    'jobs_page_url': 'https://careers.timewarner.com/TGWebHost/home.aspx?partnerid=391&siteid=36',

    'empcnt': [5001,10000]
}

class TurnerJobScraper(BrassringJobScraper):
    def __init__(self):
        super(TurnerJobScraper, self).__init__(COMPANY)
        self.soupify_search_form = True

    def get_url_from_formtext(self, x):
        s = soupify(x['JobTitle'])
        a = s.findAll('a')
        return a[1]

    def get_title_from_formtext(self, x):
        t = soupify(x['JobTitle'])
        a = t.findAll('a')
        return a[1].text

    def get_location_from_formtext(self, x):
        l = x['Location']
        l = self.parse_location(l)

        return l

def get_scraper():
    return TurnerJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
