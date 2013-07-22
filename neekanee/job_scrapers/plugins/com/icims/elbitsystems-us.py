from neekanee.jobscrapers.icims.icims import IcimsJobScraper

COMPANY = {
    'name': 'Elbit Systems of America',
    'hq': 'Fort Worth, TX',

    'ats': 'icims',

    'home_page_url': 'http://www.elbitsystems-us.com',
    'jobs_page_url': 'https://jobs-esa.icims.com/jobs/intro',

    'empcnt': [1001,5000],
}

class ElbitSystemsUsJobScraper(IcimsJobScraper):
    def __init__(self):
        super(ElbitSystemsUsJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        l = td[-2].text
        return self.parse_location(l)

def get_scraper():
    return ElbitSystemsUsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
    
