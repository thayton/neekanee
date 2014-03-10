from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'The May Institute',
    'hq': 'Randolph, MA',

    'home_page_url': 'http://www.mayinstitute.org',
    'jobs_page_url': 'https://careers-mayinstitute.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [1001,5000]
}

class MayInstituteJobScraper(IcimsJobScraper):
    def __init__(self):
        super(MayInstituteJobScraper, self).__init__(COMPANY)

def get_scraper():
    return MayInstituteJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
