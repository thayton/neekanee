import re

from neekanee.jobscrapers.kenexa.kenexa import KenexaJobScraper

COMPANY = {
    'name': 'NetApp',
    'hq': 'Sunnyvale, CA',

    'ats': 'Kenexa',
    'benefits': {'vacation': [(1,12),(2,15),(6,20),(10,25)]},

    'home_page_url': 'http://www.netapp.com',
    'jobs_page_url': 'https://careers.netapp.com/1033/ASP/TG/cim_home.asp?partnerid=25093&siteid=5100',

    'bptw_glassdoor': True,
    'gptwcom_fortune': True,

    'empcnt': [5001,10000]
}

class NetAppJobScraper(KenexaJobScraper):
    def __init__(self):
        super(NetAppJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        y = re.sub('\(.*?\)', '', td[-1].text)
        y = y.split(',')[0]
        
        return self.parse_location(y)

    def get_title_from_td(self, td):
        return td[3].text

def get_scraper():
    return NetAppJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
