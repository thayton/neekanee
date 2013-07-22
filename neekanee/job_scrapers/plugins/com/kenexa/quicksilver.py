from neekanee.jobscrapers.kenexa.kenexa import KenexaJobScraper

COMPANY = {
    'name': 'Quicksilver',
    'hq': 'Huntington Beach, CA',

    'ats': 'Kenexa',

    'home_page_url': 'http://www.quicksilver.com',
    'jobs_page_url': 'https://sjobs.brassring.com/1033/ASP/TG/cim_home.asp?partnerid=25080&siteid=5080',

    'empcnt': [5001,10000]
}

class QuicksilverJobScraper(KenexaJobScraper):
    def __init__(self):
        super(QuicksilverJobScraper, self).__init__(COMPANY)

    def get_title_from_td(self, td):
        return td[3].text

    def get_location_from_td(self, td):
        return self.parse_location(td[4].text)
    
def get_scraper():
    return QuicksilverJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
