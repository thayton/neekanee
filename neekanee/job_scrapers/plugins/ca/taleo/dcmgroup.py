from neekanee.jobscrapers.taleo.taleo import TaleoJobScraper
from neekanee.htmlparse.soupify import get_all_text

COMPANY = {
    'name': 'DCM Group',
    'hq': 'Sherwood Park, Canada',

    'home_page_url': 'http://www.dcmgroup.ca',
    'jobs_page_url': 'http://ch.tbe.taleo.net/CH01/ats/careers/jobSearch.jsp?org=DAWCO&cws=37',

    'empcnt': [51,200]
}

class DcmJobScraper(TaleoJobScraper):
    def __init__(self):
        super(DcmJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[-3].text)

    def get_desc_from_s(self, s):
        x = {'role': 'presentation'}
        t = s.find('table', attrs=x)
        return get_all_text(t)

def get_scraper():
    return DcmJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
