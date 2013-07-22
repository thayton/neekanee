from neekanee.jobscrapers.icims.icims import IcimsJobScraper

COMPANY = {
    'name': 'J. Crew',
    'hq': 'New York, NY',

    'home_page_url': 'http://www.jcrew.com',
    'jobs_page_url': 'https://jobs-jcrew.icims.com/jobs/intro?hashed=0',

    'empcnt': [5001,10000]
}

class JCrewJobScraper(IcimsJobScraper):
    def __init__(self):
        super(JCrewJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[1].text)

def get_scraper():
    return JCrewJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
