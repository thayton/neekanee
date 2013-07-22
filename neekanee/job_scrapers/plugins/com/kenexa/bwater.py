from neekanee.jobscrapers.kenexa.kenexa import KenexaJobScraper

COMPANY = {
    'name': 'Bridgewater Associates',
    'hq': 'Westport, CT',

    'ats': 'Kenexa',

    'home_page_url': 'http://www.bwater.com',
    'jobs_page_url': 'https://sjobs.brassring.com/1033/ASP/TG/cim_home.asp?partnerid=25310&siteid=5242',

    'empcnt': [1001,5000]
}

class BwaterJobScraper(KenexaJobScraper):
    def __init__(self):
        super(BwaterJobScraper, self).__init__(COMPANY)

def get_scraper():
    return BwaterJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
