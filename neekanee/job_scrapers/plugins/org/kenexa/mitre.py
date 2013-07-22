from neekanee.jobscrapers.kenexa.kenexa import KenexaJobScraper

COMPANY = {
    'name': 'MITRE',
    'hq': 'Bedford, MA',

    'ats': 'Kenexa',

    'home_page_url': 'http://www.mitre.org',
    'jobs_page_url': 'https://jobs.brassring.com/en/asp/tg/cim_home.asp?sec=1&partnerid=119&siteid=69',

    'empcnt': [5001, 10000]
}

class MitreJobScraper(KenexaJobScraper):
    def __init__(self):
        super(MitreJobScraper, self).__init__(COMPANY)

    def get_title_from_td(self, td):
        return td[3].text

    def get_location_from_td(self, td):
        return self.parse_location(td[4].text)
        
def get_scraper():
    return MitreJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
