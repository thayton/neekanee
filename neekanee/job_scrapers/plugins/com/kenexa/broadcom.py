from neekanee.jobscrapers.kenexa.kenexa import KenexaJobScraper

COMPANY = {
    'name': 'Broadcom',
    'hq': 'Irvine, CA',

    'ats': 'Kenexa',

    'home_page_url': 'http://www.broadcom.com',
    'jobs_page_url': 'https://sjobs.brassring.com/1033/ASP/TG/cim_home.asp?partnerid=25231&siteid=5283',
                      
    'empcnt': [10001]
}

class BroadcomJobScraper(KenexaJobScraper):
    def __init__(self):
        super(BroadcomJobScraper, self).__init__(COMPANY)
        self.geocoder.return_usa_only = False
        self.soupify_search_form = True

    def get_location_from_td(self, td):
        if td[-4].text.strip() == 'United States':
            l = td[-2].text + ', ' + td[-3].text + ', ' + td[-4].text
        else:
            l = td[-2].text + ', ' + td[-4].text

        return self.parse_location(l)
    
def get_scraper():
    return BroadcomJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
