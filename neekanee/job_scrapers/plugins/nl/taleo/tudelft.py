from neekanee.jobscrapers.taleo.taleo import TaleoJobScraper
from neekanee.htmlparse.soupify import get_all_text

COMPANY = {
    'name': 'Tu Delft',
    'hq': 'Delft, Netherlands',

    'home_page_url': 'http://tudelft.nl/en/',
    'jobs_page_url': 'https://tbe.taleo.net/CH09/ats/careers/jobSearch.jsp?org=FOAS&cws=7',

    'empcnt': [5001,10000]
}

class TuDelftJobScraper(TaleoJobScraper):
    def __init__(self):
        super(TuDelftJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[-1].text)

    def get_desc_from_s(self, s):
        return get_all_text(s.body)

def get_scraper():
    return TuDelftJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
