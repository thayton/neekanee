from neekanee.jobscrapers.icims.icims import IcimsJobScraper

COMPANY = {
    'name': 'Akamai',
    'hq': 'Cambridge, MA',

    'home_page_url': 'http://www.akamai.com',
    'jobs_page_url': 'https://jobs-akamai.icims.com/jobs/intro?hashed=0',

    'empcnt': [1001,5000]
}

class AkamaiJobScraper(IcimsJobScraper):
    def __init__(self):
        super(AkamaiJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[-2].text)

def get_scraper():
    return AkamaiJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
