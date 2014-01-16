from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'Orbital Sciences Corporation',
    'hq': 'Dulles, VA',

    'home_page_url': 'https://www.orbital.com/',
    'jobs_page_url': 'https://jobs-orbital.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [1001,5000],
}

class OrbitalJobScraper(IcimsJobScraper):
    def __init__(self):
        super(OrbitalJobScraper, self).__init__(COMPANY)

def get_scraper():
    return OrbitalJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
    
