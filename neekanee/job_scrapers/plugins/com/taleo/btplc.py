from neekanee.jobscrapers.taleo.taleo import TaleoJobScraper
from neekanee.htmlparse.soupify import get_all_text

COMPANY = {
    'name': 'British Telecom',
    'hq': 'London, United Kingdom',

    'ats': 'Taleo',

    'home_page_url': 'http://www.btplc.com',
    'jobs_page_url': 'https://tbe.taleo.net/CH09/ats/careers/jobSearch.jsp?org=BT&cws=1',

    'empcnt': [10001]
}

class BtJobScraper(TaleoJobScraper):
    def __init__(self):
        super(BtJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[2].text)

    def get_desc_from_s(self, s):
        h = s.find('h1')
        t = h.findParent('table')
        return get_all_text(t)

def get_scraper():
    return BtJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
