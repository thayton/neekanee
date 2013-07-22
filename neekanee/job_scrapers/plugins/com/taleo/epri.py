from neekanee.jobscrapers.taleo.taleo import TaleoJobScraper
from neekanee.htmlparse.soupify import get_all_text

COMPANY = {
    'name': 'Electric Power Research Institute (EPRI)',
    'hq': 'Palo Alto, CA',

    'ats': 'Taleo',

    'home_page_url': 'http://www.epri.com',
    'jobs_page_url': 'http://ch.tbe.taleo.net/CH05/ats/careers/jobSearch.jsp?org=EPRI&cws=1',

    'empcnt': [501,1000]
}

class EpriJobScraper(TaleoJobScraper):
    def __init__(self):
        super(EpriJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[-1].text)

    def get_desc_from_s(self, s):
        d = s.find('div', id='main')
        return get_all_text(d)

def get_scraper():
    return EpriJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
