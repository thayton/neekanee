from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'LogiXML',
    'hq': 'McLean, VA',

    'contact': 'Jobs@logixml.com',

    'home_page_url': 'http://www.logixml.com',
    'jobs_page_url': 'https://careers-logixml.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [51,200]
}

class LogiXmlJobScraper(IcimsJobScraper):
    def __init__(self):
        super(LogiXmlJobScraper, self).__init__(COMPANY)

def get_scraper():
    return LogiXmlJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()

