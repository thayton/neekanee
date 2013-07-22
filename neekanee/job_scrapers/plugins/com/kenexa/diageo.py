from neekanee.jobscrapers.kenexa.kenexa import KenexaJobScraper

COMPANY = {
    'name': 'Diageo',
    'hq': 'London, United Kingdom',

    'home_page_url': 'http://www.diageo.com',
    'jobs_page_url': 'https://sjobs.brassring.com/1033/ASP/TG/cim_home.asp?partnerid=11729&siteid=208',

    'empcnt': [10001]
}

class DiageoJobScraper(KenexaJobScraper):
    def __init__(self):
        super(DiageoJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        l = td[5].text + ', ' + td[4].text
        return self.parse_location(l)
    
def get_scraper():
    return DiageoJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
