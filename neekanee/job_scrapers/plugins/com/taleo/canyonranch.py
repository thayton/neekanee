from neekanee.jobscrapers.taleo.taleo import TaleoJobScraper
from neekanee.htmlparse.soupify import get_all_text

import re

COMPANY = {
    'name': 'Canyon Ranch',
    'hq': 'Tucson, AZ',

    'ats': 'Taleo',

    'home_page_url': 'http://www.canyonranch.com',
    'jobs_page_url': 'http://tbe.taleo.net/CH08/ats/careers/jobSearch.jsp?org=CRTUCSON&cws=1',

    'empcnt': [501,1000]
}

class CanyonRanchJobScraper(TaleoJobScraper):
    def __init__(self):
        super(CanyonRanchJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        l = re.sub(r'Corporate -', '', td[1].text)
        return self.parse_location(l)

    def get_desc_from_s(self, s):
        x = {'role': 'presentation'}
        t = s.find('table', attrs=x)
        return get_all_text(t)

def get_scraper():
    return CanyonRanchJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
