from neekanee.jobscrapers.icims.icims import IcimsJobScraper

COMPANY = {
    'name': 'Finning (Canada)',
    'hq': 'Edmonton, Canada',

    'home_page_url': 'http://www.finning.ca',
    'jobs_page_url': 'https://careers-finning.icims.com/jobs/intro?hashed=0',

    'empcnt': [5001,10000]
}

class FinningJobScraper(IcimsJobScraper):
    def __init__(self):
        super(FinningJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        l = td[-3].text + ', ' + td[-4].text
        return self.parse_location(l)

def get_scraper():
    return FinningJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
