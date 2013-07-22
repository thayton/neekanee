from neekanee.jobscrapers.icims.icims import IcimsJobScraper

COMPANY = {
    'name': 'Jacobs Technology',
    'hq': 'Tullahoma, TN',

    'ats': 'icims',

    'home_page_url': 'http://www.jacobstechnology.com',
    'jobs_page_url': 'https://jacobsexternal-jacobstechnology.icims.com/jobs/intro',

    'empcnt': [1001,5000]
}

class JacobsJobScraper(IcimsJobScraper):
    def __init__(self):
        super(JacobsJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[-2].text)

def get_scraper():
    return JacobsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
