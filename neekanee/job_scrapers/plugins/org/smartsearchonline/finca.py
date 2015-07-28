from neekanee.jobscrapers.taleo.taleo import TaleoJobScraper
from neekanee.htmlparse.soupify import get_all_text

COMPANY = {
    'name': 'FINCA',
    'hq': 'Washington, DC',

    'ats': 'Taleo',

    'home_page_url': 'http://www.finca.org',
    'jobs_page_url': 'http://tbe.taleo.net/CH06/ats/careers/jobSearch.jsp?org=FINCA&cws=1',

    'empcnt': [5001,10000]
}

class FincaJobScraper(TaleoJobScraper):
    def __init__(self):
        super(FincaJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        l = td[1].text
        if len(l.strip()) > 0:
            return self.parse_location(td[1].text)
        else:
            return None

def get_scraper():
    return FincaJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
