from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'BRMI Consulting',
    'hq': 'Columbia, MD',

    'ats': 'icims',

    'contact': 'careers@brmiconsulting.com',

    'home_page_url': 'http://public.brmiconsulting.com',
    'jobs_page_url': 'https://careers-brmi.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [51,200]
}

class BrmiJobScraper(IcimsJobScraper):
    def __init__(self):
        super(BrmiJobScraper, self).__init__(COMPANY)

def get_scraper():
    return BrmiJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
