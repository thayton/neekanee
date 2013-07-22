from neekanee.jobscrapers.kenexa.kenexa import KenexaJobScraper

COMPANY = {
    'name': 'Excelis',
    'hq': 'McLean, VA',

    'ats': 'Kenexa',

    'home_page_url': 'http://www.exelis.com',
    'jobs_page_url': 'https://sjobs.brassring.com/1033/ASP/TG/cim_home.asp?partnerid=25326&siteid=5443',

    'empcnt': [10001]
}

class ExelisJobScraper(KenexaJobScraper):
    def __init__(self):
        super(ExelisJobScraper, self).__init__(COMPANY)
        self.soupify_search_form = True

    def get_title_from_td(self, td):
        return td[5].text

    def get_location_from_td(self, td):
        return self.parse_location(td[3].text)
    
def get_scraper():
    return ExelisJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
