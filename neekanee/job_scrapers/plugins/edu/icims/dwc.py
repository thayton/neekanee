from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'Daniel Webster College ',
    'hq': 'Nashua, NH',

    'ats': 'icims',

    'home_page_url': 'http://www.dwc.edu',
    'jobs_page_url': 'https://careers-dwc.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [51,200]
}

class DwcJobScraper(IcimsJobScraper):
    def __init__(self):
        super(DwcJobScraper, self).__init__(COMPANY)

def get_scraper():
    return DwcJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
