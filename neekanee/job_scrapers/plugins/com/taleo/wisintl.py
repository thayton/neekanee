from neekanee.jobscrapers.taleo.taleo import TaleoJobScraper
from neekanee.htmlparse.soupify import get_all_text

COMPANY = {
    'name': 'WIS International',
    'hq': 'San Diego, CA',

    'ats': 'Taleo',

    'home_page_url': 'http://www.wisintl.com',
    'jobs_page_url': 'https://sj.tbe.taleo.net/CH16/ats/careers/jobSearch.jsp?org=WISINTL&cws=1',

    'empcnt': [10001]
}

class WisIntlJobScraper(TaleoJobScraper):
    def __init__(self):
        super(WisIntlJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[-1].text)

    def get_desc_from_s(self, s):
        h = s.find('h1')
        t = h.findParent('table')
        return get_all_text(t)

def get_scraper():
    return WisIntlJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
