from neekanee.jobscrapers.taleo.taleo import TaleoJobScraper
from neekanee.htmlparse.soupify import get_all_text

COMPANY = {
    'name': 'CARE',
    'hq': 'Atlanta, GA',

    'ats': 'Taleo',

    'home_page_url': 'http://www.care.org',
    'jobs_page_url': 'https://tbe.taleo.net/CH05/ats/careers/jobSearch.jsp?org=CAREUSA&cws=1',

    'empcnt': [5001,10000]
}

class CareJobScraper(TaleoJobScraper):
    def __init__(self):
        super(CareJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        l = td[-1].text
        if len(l.strip()) > 0:
            return self.parse_location(td[-1].text)
        else:
            return None

def get_scraper():
    return CareJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
