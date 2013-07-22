from neekanee.jobscrapers.icims.icims import IcimsJobScraper

COMPANY = {
    'name': 'North American Construction Group',
    'hq': 'Acheson, Canada',

    'home_page_url': 'http://www.nacg.ca',
    'jobs_page_url': 'http://careers-nacg.icims.com/',

    'empcnt': [1001,5000]
}

class NacgJobScraper(IcimsJobScraper):
    def __init__(self):
        super(NacgJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[-2].text)

def get_scraper():
    return NacgJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
