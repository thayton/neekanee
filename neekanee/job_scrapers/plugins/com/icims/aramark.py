from neekanee.jobscrapers.icims.icims import IcimsJobScraper

COMPANY = {
    'name': 'Aramark',
    'hq': 'Philadelphia, PA',

    'home_page_url': 'http://www.aramark.com',
    'jobs_page_url': 'https://allcareers-aramark.icims.com/jobs/intro?hashed=0',

    'empcnt': [10001]
}

class AramarkJobScraper(IcimsJobScraper):
    def __init__(self):
        super(AramarkJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[-3].text)

def get_scraper():
    return AramarkJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
