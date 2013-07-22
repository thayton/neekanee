from neekanee.jobscrapers.icims.icims import IcimsJobScraper

COMPANY = {
    'name': 'Orbital Sciences Corporation',
    'hq': 'Dulles, VA',

    'home_page_url': 'https://www.orbital.com/',
    'jobs_page_url': 'https://jobs-orbital.icims.com/jobs/intro',

    'empcnt': [1001,5000],
}

class OrbitalJobScraper(IcimsJobScraper):
    def __init__(self):
        super(OrbitalJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        l = td[2].text
        return self.parse_location(l)

def get_scraper():
    return OrbitalJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
    
