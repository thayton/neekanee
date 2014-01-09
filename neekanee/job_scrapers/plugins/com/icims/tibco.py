from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'TIBCO',
    'hq': 'Palo Alto, CA',

    'ats': 'icims',

    'home_page_url': 'http://www.tibco.com',
    'jobs_page_url': 'https://usa-tibcosoftware.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [1001,5000]
}

class TibcoJobScraper(IcimsJobScraper):
    def __init__(self):
        super(TibcoJobScraper, self).__init__(COMPANY)

def get_scraper():
    return TibcoJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
