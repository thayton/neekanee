from neekanee.jobscrapers.taleo.taleo import TaleoJobScraper
from neekanee.htmlparse.soupify import get_all_text

COMPANY = {
    'name': 'Transcore',
    'hq': 'Hummelstown, PA',

    'home_page_url': 'http://transcore.com',
    'jobs_page_url': 'http://ch.tbe.taleo.net/CH03/ats/careers/jobSearch.jsp?org=ROPERSW&cws=1',

    'empcnt': [1001,5000]
}

class TranscoreJobScraper(TaleoJobScraper):
    def __init__(self):
        super(TranscoreJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[1].text)

    def get_desc_from_s(self, s):
        hr = s.find('hr')
        t = hr.findParent('table')
        return get_all_text(t)

def get_scraper():
    return TranscoreJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
