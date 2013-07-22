from neekanee.jobscrapers.icims.icims import IcimsJobScraper

COMPANY = {
    'name': 'Solera Networks',
    'hq': 'South Jordan, Utah',

    'home_page_url': 'http://www.soleranetworks.com',
    'jobs_page_url': 'https://careers-soleranetworks.icims.com/jobs/intro?hashed=0',

    'empcnt': [51,200]
}

class SoleraNetworksJobScraper(IcimsJobScraper):
    def __init__(self):
        super(SoleraNetworksJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[-2].text)

def get_scraper():
    return SoleraNetworksJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
