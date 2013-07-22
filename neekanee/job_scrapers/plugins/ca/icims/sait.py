from neekanee.jobscrapers.icims.icims import IcimsJobScraper

COMPANY = {
    'name': 'SAIT Polytechnic',
    'hq': 'Calgary, Canada',

    'home_page_url': 'http://www.sait.ca',
    'jobs_page_url': 'https://careers-sait.icims.com/jobs/intro',

    'empcnt': [1001,5000]
}

class SaitJobScraper(IcimsJobScraper):
    def __init__(self):
        super(SaitJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[-2].text)

def get_scraper():
    return SaitJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
