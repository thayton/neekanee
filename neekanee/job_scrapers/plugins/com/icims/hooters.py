from neekanee.jobscrapers.icims.icims import IcimsJobScraper

COMPANY = {
    'name': 'Hooters of America',
    'hq': 'Atlanta, GA',

    'ats': 'Icims',

    'home_page_url': 'http://www.hooters.com',
    'jobs_page_url': 'https://careershub-hooters.icims.com/',

    'empcnt': [51,200]
}

class HootersJobScraper(IcimsJobScraper):
    def __init__(self):
        super(HootersJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[-2].text)

def get_scraper():
    return HootersJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
