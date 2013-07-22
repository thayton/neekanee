from neekanee.jobscrapers.icims.icims import IcimsJobScraper

COMPANY = {
    'name': 'Rapid7',
    'hq': 'Boston, MA',

    'home_page_url': 'http://www.rapid7.com',
    'jobs_page_url': 'https://careers-rapid7.icims.com/jobs/intro?hashed=0',

    'empcnt': [201,500]
}

class Rapid7JobScraper(IcimsJobScraper):
    def __init__(self):
        super(Rapid7JobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[2].text)

def get_scraper():
    return Rapid7JobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
