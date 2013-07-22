from neekanee.jobscrapers.icims.icims import IcimsJobScraper

COMPANY = {
    'name': 'Marathon Oil Corporation',
    'hq': 'Houston, TX',

    'home_page_url': 'http://www.marathonoil.com',
    'jobs_page_url': 'https://jobs-marathon.icims.com/jobs/intro?hashed=0',

    'empcnt': [1001,5000]
}

class MarathonOilJobScraper(IcimsJobScraper):
    def __init__(self):
        super(MarathonOilJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[-1].text)

def get_scraper():
    return MarathonOilJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
