from neekanee.jobscrapers.kenexa.kenexa import KenexaJobScraper

COMPANY = {
    'name': 'Susquehanna International Group',
    'hq': 'Bala Cynwyd, PA',

    'ats': 'Kenexa',
    'benefits': {'vacation': []},

    'home_page_url': 'http://www.sig.com',
    'jobs_page_url': 'https://sjobs.brassring.com/1033/ASP/TG/cim_home.asp?partnerid=16005&siteid=5056',

    'empcnt': [1001,5000]
}

class SigJobScraper(KenexaJobScraper):
    def __init__(self):
        super(SigJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[3].text)

def get_scraper():
    return SigJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
