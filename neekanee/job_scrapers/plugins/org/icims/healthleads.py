from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'Health Leads',
    'hq': 'Boston, MA',

    'ats': 'icims',

    'home_page_url': 'http://www.healthleadsusa.org',
    'jobs_page_url': 'https://careers-healthleads.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [11,50]
}

class HealthLeadsJobScraper(IcimsJobScraper):
    def __init__(self):
        super(HealthLeadsJobScraper, self).__init__(COMPANY)

def get_scraper():
    return HealthLeadsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
