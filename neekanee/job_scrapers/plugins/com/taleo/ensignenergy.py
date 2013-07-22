from neekanee.jobscrapers.taleo.taleo2 import TaleoJobScraper

COMPANY = {
    'name': 'Ensign Energy Services',
    'hq': 'Calgary, Canada',

    'home_page_url': 'http://www.ensignenergy.com',
    'jobs_page_url': 'https://ensignenergy.taleo.net/careersection/2/jobsearch.ftl?lang=en',

    'empcnt': [1001,5000]
}

class EnsignEnergyJobScraper(TaleoJobScraper):
    def __init__(self):
        super(EnsignEnergyJobScraper, self).__init__(COMPANY)

def get_scraper():
    return EnsignEnergyJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
