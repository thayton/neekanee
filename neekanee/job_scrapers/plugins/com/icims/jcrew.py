from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'J. Crew',
    'hq': 'New York, NY',

    'home_page_url': 'http://www.jcrew.com',
    'jobs_page_url': 'https://jobs-jcrew.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [5001,10000]
}

class JCrewJobScraper(IcimsJobScraper):
    def __init__(self):
        super(JCrewJobScraper, self).__init__(COMPANY)

def get_scraper():
    return JCrewJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
