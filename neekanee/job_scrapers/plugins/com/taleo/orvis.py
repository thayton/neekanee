import re

from neekanee.jobscrapers.taleo.taleo import TaleoJobScraper
from neekanee.htmlparse.soupify import get_all_text

COMPANY = {
    'name': 'Orvis',
    'hq': 'Sunderland, VT',

    'ats': 'Taleo',

    'home_page_url': 'http://www.orvis.com/',
    'jobs_page_url': 'https://sj.tbe.taleo.net/CH14/ats/careers/jobSearch.jsp?org=ORVIS&cws=1',

    'empcnt': [1001,5000]
}

class OrvisJobScraper(TaleoJobScraper):
    def __init__(self):
        super(OrvisJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        l = re.split(r'&#40;', td[1].text)[0]
        l = l.partition('-')
        l = ''.join(['%s' % x for x in l[:3]])

        return self.parse_location(l)

    def get_desc_from_s(self, s):
        t = s.h1.findParent('table')
        return get_all_text(t)

def get_scraper():
    return OrvisJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
