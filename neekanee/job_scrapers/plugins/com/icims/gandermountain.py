from neekanee.jobscrapers.icims.icims import IcimsJobScraper

COMPANY = {
    'name': 'Gander Mountain',
    'hq': 'St Paul, MN',

    'home_page_url': 'https://www.gandermountain.com/',
    'jobs_page_url': 'https://jobs-gandermountain.icims.com/jobs/intro',

    'empcnt': [5001,10000],
}

class GanderMountainJobScraper(IcimsJobScraper):
    def __init__(self):
        super(GanderMountainJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        l = td[2].text
        return self.parse_location(l)

def get_scraper():
    return GanderMountainJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
    
