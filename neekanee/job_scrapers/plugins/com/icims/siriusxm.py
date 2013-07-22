from neekanee.jobscrapers.icims.icims import IcimsJobScraper

COMPANY = {
    'name': 'SiriusXM',
    'hq': 'New York, NY',

    'ats': 'icims',

    'home_page_url': 'http://www.siriusxm.com',
    'jobs_page_url': 'https://careers-siriusxm.icims.com/jobs/intro',

    'empcnt': [1001,5000]
}

class SiriusXmJobScraper(IcimsJobScraper):
    def __init__(self):
        super(SiriusXmJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[-1].text)

def get_scraper():
    return SiriusXmJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
