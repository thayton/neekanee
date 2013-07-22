from neekanee.jobscrapers.taleo.taleo import TaleoJobScraper
from neekanee.htmlparse.soupify import get_all_text

COMPANY = {
    'name': 'FHI 360',
    'hq': 'Durham, NC',

    'home_page_url': 'http://www.fhi360.org',
    'jobs_page_url': 'https://tbe.taleo.net/CH12/ats/careers/jobSearch.jsp?org=FHI&cws=1',

    'empcnt': [1001,5000]
}

class Fhi360JobScraper(TaleoJobScraper):
    def __init__(self):
        super(Fhi360JobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        l = td[3].text + ', ' + td[2].text
        return self.parse_location(l)

    def get_desc_from_s(self, s):
        h = s.find('h1')
        t = h.findParent('table')
        return get_all_text(t)

def get_scraper():
    return Fhi360JobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
