from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'iRobot',
    'hq': 'Bedford, MA',

    'ats': 'icims',

    'home_page_url': 'http://www.irobot.com',
    'jobs_page_url': 'https://careers-irobot.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [201,500],
}

locations = (
    ('US-MA', lambda x: x + 'Bedford'),
    ('US-NC', lambda x: x + 'Durham'),
    ('US-CA', lambda x: x + 'San Luis Obispo'),
    ('US-FL', lambda x: x + 'Miami'),
    ('US-VA', lambda x: x + 'Arlington'),
)

# Locations in table only specify coutry state (US-MA-)
# so we have to fill in the locations based on the companies
# list of office locations http://www.irobot.com/sp.cfm?pageid=89
def full_location(text):
    for prefix,func in locations:
        if text == prefix:
            return func(text)

    return None

class IRobotJobScraper(IcimsJobScraper):
    def __init__(self):
        super(IRobotJobScraper, self).__init__(COMPANY)

    def get_location_from_div(self, div):
        y = {'itemprop': 'address'}
        p = div.find('span', attrs=y)
        l = full_location(p.text)

        if l is None:
            return None

        return self.parse_location(l)

def get_scraper():
    return IRobotJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
    
