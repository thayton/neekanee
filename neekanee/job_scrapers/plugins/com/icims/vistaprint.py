from neekanee.jobscrapers.icims.icims import IcimsJobScraper

COMPANY = {
    'name': 'Vistaprint',
    'hq': 'Paris, France',

    'ats': 'icims',

    'home_page_url': 'http://www.vistaprint.com',
    'jobs_page_url': 'https://jobs-vistaprint.icims.com/jobs/intro?hashed=0',

    'empcnt': [1001,5000]
}

class VistaPrintJobScraper(IcimsJobScraper):
    def __init__(self):
        super(VistaPrintJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[-1].text)

def get_scraper():
    return VistaPrintJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
