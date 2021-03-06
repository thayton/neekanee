from neekanee.jobscrapers.taleo.taleo import TaleoJobScraper
from neekanee.htmlparse.soupify import get_all_text

COMPANY = {
    'name': 'Adelphi University',
    'hq': 'Garden City, NY',

    'ats': 'Taleo',

    'home_page_url': 'http://www.adelphi.edu',
    'jobs_page_url': 'http://ch.tbe.taleo.net/CH01/ats/careers/jobSearch.jsp?org=ADELPHI&cws=1',

    'empcnt': [1001,5000]
}

class AdelphiJobScraper(TaleoJobScraper):
    def __init__(self):
        super(AdelphiJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[-1].text)

    def get_desc_from_s(self, s):
        h = s.find('h1')
        t = h.findParent('table')
        return get_all_text(t)

def get_scraper():
    return AdelphiJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
