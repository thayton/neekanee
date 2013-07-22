from neekanee.jobscrapers.icims.icims import IcimsJobScraper

COMPANY = {
    'name': 'Rearden Commerce',
    'hq': 'Foster City, CA',

    'home_page_url': 'http://www.reardencommerce.com/',
    'jobs_page_url': 'https://careers-reardencommerce.icims.com/jobs/intro',

    'empcnt': [501,1000]
}

class ReardenCommerceJobScraper(IcimsJobScraper):
    def __init__(self):
        super(ReardenCommerceJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        x = {'itemprop': 'address'}
        p = td[-1].find('span', attrs=x)
        l = self.parse_location(p.text)
        return l

def get_scraper():
    return ReardenCommerceJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
