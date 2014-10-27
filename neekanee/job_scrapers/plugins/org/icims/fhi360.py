from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'FHI 360',
    'hq': 'Durham, NC',

    'home_page_url': 'http://www.fhi360.org',
    'jobs_page_url': 'https://jobs-fhi360.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [1001,5000]
}

class Fhi360JobScraper(IcimsJobScraper):
    def __init__(self):
        super(Fhi360JobScraper, self).__init__(COMPANY)

def get_scraper():
    return Fhi360JobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
