from neekanee.jobscrapers.kenexa.kenexa import KenexaJobScraper

COMPANY = {
    'name': 'Masco Cabinetry',
    'hq': 'Ann Arbor, MI',

    'home_page_url': 'http://www.mascocabinetry.com',
    'jobs_page_url': 'https://sjobs.brassring.com/1033/asp/tg/cim_home.asp?partnerid=25204&siteid=5219',

    'empcnt': [1001,5000]
}

class MascoCabinetryJobScraper(KenexaJobScraper):
    def __init__(self):
        super(MascoCabinetryJobScraper, self).__init__(COMPANY)
        self.soupify_search_form = True

    def get_title_from_td(self, td):
        return td[3].text

    def get_location_from_td(self, td):
        l = ', '.join(['%s' % x.text for x in td[-4:-1]])
        return self.parse_location(l)
    
def get_scraper():
    return MascoCabinetryJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
