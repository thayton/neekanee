from neekanee.jobscrapers.taleo.taleo import TaleoJobScraper
from neekanee.htmlparse.soupify import get_all_text

COMPANY = {
    'name': 'Burson Marsteller',
    'hq': 'New York, NY',

    'home_page_url': 'http://www.bm.com',
    'jobs_page_url': 'http://tbe.taleo.net/CH03/ats/careers/jobSearch.jsp?org=BM&cws=1',

    'empcnt': [1001,5000]
}

class BursonMarstellerJobScraper(TaleoJobScraper):
    def __init__(self):
        super(BursonMarstellerJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[-1].text)

def get_scraper():
    return BursonMarstellerJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
