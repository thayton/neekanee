import re
from neekanee.jobscrapers.icims.icims2 import IcimsJobScraper

COMPANY = {
    'name': 'North American Construction Group',
    'hq': 'Acheson, Canada',

    'home_page_url': 'http://www.nacg.ca',
    'jobs_page_url': 'http://careers-nacg.icims.com/jobs/intro?in_iframe=1',

    'empcnt': [1001,5000]
}

class NacgJobScraper(IcimsJobScraper):
    def __init__(self):
        super(NacgJobScraper, self).__init__(COMPANY)

    def get_location_from_div(self, div):
        r = re.compile(r'^Job City:')
        t = div.find(text=r)
        d = t.findParent('div')
        l = self.parse_location(d.contents[-1])
        return l

def get_scraper():
    return NacgJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
