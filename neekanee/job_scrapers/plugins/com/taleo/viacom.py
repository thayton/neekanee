from neekanee.jobscrapers.taleo.taleo import TaleoJobScraper
from neekanee.htmlparse.soupify import get_all_text

COMPANY = {
    'name': 'Viacom',
    'hq': 'New York, NY',

    'home_page_url': 'http://www.viacom.com',
    'jobs_page_url': 'http://tbe.taleo.net/CH05/ats/careers/jobSearch.jsp?org=MTVNETWORKS&cws=1',

    'empcnt': [1001,5000]
}

class ViacomJobScraper(TaleoJobScraper):
    def __init__(self):
        super(ViacomJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[1].text)

    def get_desc_from_s(self, s):
        d = s.find('div', id='content')
        return get_all_text(d)

def get_scraper():
    return ViacomJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
