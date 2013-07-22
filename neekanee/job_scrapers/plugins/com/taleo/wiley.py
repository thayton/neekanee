from neekanee.jobscrapers.taleo.taleo import TaleoJobScraper
from neekanee.htmlparse.soupify import get_all_text

COMPANY = {
    'name': 'John Wiley and Sons',
    'hq': 'Hoboken, NJ',

    'home_page_url': 'http://www.wiley.com',
    'jobs_page_url': 'http://tbe.taleo.net/CH04/ats/careers/jobSearch.jsp?org=WILEY&cws=1',

    'empcnt': [1001,5000]
}

class WileyJobScraper(TaleoJobScraper):
    def __init__(self):
        super(WileyJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[1].text)

    def get_desc_from_s(self, s):
        d = s.find('div', id='page')
        return get_all_text(d.table)

def get_scraper():
    return WileyJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
