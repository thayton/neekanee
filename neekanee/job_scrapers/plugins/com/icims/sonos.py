from neekanee.jobscrapers.icims.icims import IcimsJobScraper

COMPANY = {
    'name': 'Sonos',
    'hq': 'Santa Barbara, CA',

    'home_page_url': 'http://www.sonos.com',
    'jobs_page_url': 'https://jobs-sonos.icims.com/jobs/intro',

    'empcnt': [201,500]
}

class SonosJobScraper(IcimsJobScraper):
    def __init__(self):
        super(SonosJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[-1].text)

def get_scraper():
    return SonosJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
