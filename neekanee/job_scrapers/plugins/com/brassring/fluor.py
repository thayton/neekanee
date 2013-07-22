from neekanee.jobscrapers.brassring.brassring import BrassringJobScraper
from neekanee.htmlparse.soupify import soupify

COMPANY = {
    'name': 'Fluor',
    'hq': 'Irving, TX',

    'home_page_url': 'http://www.fluor.com',
    'jobs_page_url': 'https://sjobs.brassring.com/tgwebhost/home.aspx?partnerid=511&siteid=231',

    'empcnt': [10001]
}

class FluorJobScraper(BrassringJobScraper):
    def __init__(self):
        super(FluorJobScraper, self).__init__(COMPANY)
        self.soupify_search_form = True

    def get_url_from_formtext(self, x):
        s = soupify(x['JobTitle'])
        return s.findAll('a')[-1]

    def get_title_from_formtext(self, x):
        s = soupify(x['JobTitle'])
        return s.findAll('a')[-1].text

    def get_location_from_formtext(self, x):
        l = x['Location'] + ', ' + x['FORMTEXT41'] + ', ' + x['FORMTEXT40']
        l = self.parse_location(l)

        return l

def get_scraper():
    return FluorJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
