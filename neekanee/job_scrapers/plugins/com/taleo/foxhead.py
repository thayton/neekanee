from neekanee.jobscrapers.taleo.taleo import TaleoJobScraper
from neekanee.htmlparse.soupify import get_all_text

COMPANY = {
    'name': 'Fox Head, Inc',
    'hq': 'Irvine, CA',

    'ats': 'Taleo',

    'home_page_url': 'http://www.foxhead.com',
    'jobs_page_url': 'http://tbe.taleo.net/NA3/ats/careers/jobSearch.jsp?org=FOXHEAD&cws=1',

    'empcnt': [201,500]
}

class FoxheadJobScraper(TaleoJobScraper):
    def __init__(self):
        super(FoxheadJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[-1].text)

    def get_desc_from_s(self, s):
        x = {'role': 'presentation'}
        t = s.find('table', attrs=x)
        return get_all_text(t)

def get_scraper():
    return FoxheadJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
