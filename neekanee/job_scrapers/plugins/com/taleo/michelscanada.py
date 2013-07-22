from neekanee.jobscrapers.taleo.taleo import TaleoJobScraper
from neekanee.htmlparse.soupify import get_all_text

COMPANY = {
    'name': 'Michels Canada',
    'hq': 'Nisku, Canada',

    'home_page_url': 'http://www.michelscanada.com',
    'jobs_page_url': 'https://tbe.taleo.net/CH07/ats/careers/jobSearch.jsp?org=MICHELSCORP&cws=1',

    'empcnt': [11,50]
}

class MichelsCanadaJobScraper(TaleoJobScraper):
    def __init__(self):
        super(MichelsCanadaJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[-1].text)

    def get_desc_from_s(self, s):
        x = {'role': 'presentation'}
        t = s.find('table', attrs=x)
        return get_all_text(t)

def get_scraper():
    return MichelsCanadaJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
