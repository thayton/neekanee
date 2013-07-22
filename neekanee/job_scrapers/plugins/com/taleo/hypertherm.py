from neekanee.jobscrapers.taleo.taleo import TaleoJobScraper
from neekanee.htmlparse.soupify import soupify, get_all_text

COMPANY = {
    'name': 'Hypertherm',
    'hq': 'Hanover, NH',

    'ats': 'Taleo',

    'home_page_url': 'http://www.hypertherm.com',
    'jobs_page_url': 'http://tbe.taleo.net/CH12/ats/careers/jobSearch.jsp?org=HYPERTHERM&cws=1',

    'empcnt': [1001,5000]
}

class HyperthermJobScraper(TaleoJobScraper):
    def __init__(self):
        super(HyperthermJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[-1].text)

    def get_desc_from_s(self, s):
        d = s.find('div', id='cntWrap')
        return get_all_text(d)

def get_scraper():
    return HyperthermJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
