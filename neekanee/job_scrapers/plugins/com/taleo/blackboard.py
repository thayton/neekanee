from neekanee.jobscrapers.taleo.taleo import TaleoJobScraper
from neekanee.htmlparse.soupify import get_all_text

COMPANY = {
    'name': 'Blackboard',
    'hq': 'Washington, DC',

    'ats': 'Taleo',

    'home_page_url': 'http://www.blackboard.com',
    'jobs_page_url': 'http://tbe.taleo.net/NA7/ats/careers/jobSearch.jsp?org=BLACKBOARD&cws=8',

    'empcnt': [1001,5000]
}

class BlackBoardJobScraper(TaleoJobScraper):
    def __init__(self):
        super(BlackBoardJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[-2].text)

    def get_desc_from_s(self, s):
        x = {'role': 'presentation'}
        t = s.find('table', attrs=x)
        return get_all_text(t)

def get_scraper():
    return BlackBoardJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
