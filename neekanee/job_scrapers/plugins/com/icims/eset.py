from neekanee.jobscrapers.icims.icims import IcimsJobScraper

COMPANY = {
    'name': 'ESET',
    'hq': 'Bratislava, Slovak Republic',

    'home_page_url': 'http://www.eset.com',
    'jobs_page_url': 'https://globalcareers-eset.icims.com/jobs/intro?hashed=0',

    'empcnt': [1001,5000]
}

class EsetJobScraper(IcimsJobScraper):
    def __init__(self):
        super(EsetJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[-2].text)

def get_scraper():
    return EsetJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
