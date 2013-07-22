from neekanee.jobscrapers.kenexa.kenexa import KenexaJobScraper

COMPANY = {
    'name': 'Jacob Leinenkugel Brewing Company',
    'hq': 'Chippewa Falls, WI',

    'home_page_url': 'https://leinie.com',
    'jobs_page_url': 'https://sjobs.brassring.com/1033/ASP/TG/cim_home.asp?partnerid=25317&siteid=5540',

    'empcnt': [51,200]
}

class LeinenkugelJobScraper(KenexaJobScraper):
    def __init__(self):
        super(LeinenkugelJobScraper, self).__init__(COMPANY)

    def get_title_from_td(self, td):
        return td[3].text

    def get_location_from_td(self, td):
        l = ', '.join(['%s' % x.text for x in td[-4:-1]])
        return self.parse_location(l)
    
def get_scraper():
    return LeinenkugelJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
