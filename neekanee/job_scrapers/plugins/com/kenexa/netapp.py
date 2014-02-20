from neekanee.jobscrapers.brassring.brassring import BrassringJobScraper
from neekanee.htmlparse.soupify import soupify

COMPANY = {
    'name': 'NetApp',
    'hq': 'Sunnyvale, CA',

    'ats': 'Kenexa',

    'home_page_url': 'http://www.netapp.com',
    'jobs_page_url': 'https://careers.netapp.com/tgwebhost/home.aspx?partnerid=25093&siteid=5100',

    'empcnt': [5001,10000]
}

class NetAppJobScraper(BrassringJobScraper):
    def __init__(self):
        super(NetAppJobScraper, self).__init__(COMPANY)
        self.soupify_search_form = True

    def get_url_from_formtext(self, x):
        s = soupify(x['AutoReq'])
        return s.a

    def get_title_from_formtext(self, x):
        return x['FORMTEXT2']

    def get_location_from_formtext(self, x):
        l = x['FORMTEXT3']
        l = self.parse_location(l)

        return l

def get_scraper():
    return NetAppJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
