from neekanee.jobscrapers.taleo.taleo import TaleoJobScraper
from neekanee.htmlparse.soupify import get_all_text

COMPANY = {
    'name': 'LGS Innovations',
    'hq': 'Herndon, VA',

    'home_page_url': 'http://www.lgsinnovations.com',
    'jobs_page_url': 'http://tbe.taleo.net/CH04/ats/careers/jobSearch.jsp?org=GOVCOLUCENT&cws=1',

    'empcnt': [501,1000]
}

class LgsInnovationsJobScraper(TaleoJobScraper):
    def __init__(self):
        super(LgsInnovationsJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[2].text)

    def get_desc_from_s(self, s):
        return get_all_text(s.html.body.table)

def get_scraper():
    return LgsInnovationsJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
