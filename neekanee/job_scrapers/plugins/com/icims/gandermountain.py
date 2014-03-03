from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'Gander Mountain',
    'hq': 'St Paul, MN',

    'home_page_url': 'https://www.gandermountain.com/',
    'jobs_page_url': 'https://jobs-gandermountain.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [5001,10000],
}

class GanderMountainJobScraper(IcimsJobScraper):
    def __init__(self):
        super(GanderMountainJobScraper, self).__init__(COMPANY)

def get_scraper():
    return GanderMountainJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
    
