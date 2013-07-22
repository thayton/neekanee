from neekanee.jobscrapers.icims.icims import IcimsJobScraper

COMPANY = {
    'name': 'Enterprise Rent-A-Car',
    'hq': 'St. Louis, MO',

    'ats': 'icims',

    'home_page_url': 'http://www.enterprise.com',
    'jobs_page_url': 'https://us-erac.icims.com/jobs/search?ss=1',

    'empcnt': [10001]
}

class EnterpriseJobScraper(IcimsJobScraper):
    def __init__(self):
        super(EnterpriseJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[-2].text)

def get_scraper():
    return EnterpriseJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
