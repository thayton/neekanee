from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'Elbit Systems of America',
    'hq': 'Fort Worth, TX',

    'ats': 'icims',

    'home_page_url': 'http://www.elbitsystems-us.com',
    'jobs_page_url': 'https://jobs-esa.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [1001,5000],
}

class ElbitSystemsUsJobScraper(IcimsJobScraper):
    def __init__(self):
        super(ElbitSystemsUsJobScraper, self).__init__(COMPANY)

def get_scraper():
    return ElbitSystemsUsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
    
