from neekanee.jobscrapers.kenexa.kenexa import KenexaJobScraper
import re

COMPANY = {
    'name': 'ManTech',
    'hq': 'Fairfax, VA',

    'home_page_url': 'http://www.mantech.com',
    'jobs_page_url': 'http://jobs.brassring.com/1033/ASP/TG/cim_home.asp?partnerid=10696&siteid=45',

    'empcnt': [5001,10000]
}

class ManTechJobScraper(KenexaJobScraper):
    def __init__(self):
        super(ManTechJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        if len(td) == 0:
            return None
        else:
            return self.parse_location(td[-4].text)

def get_scraper():
    return ManTechJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
