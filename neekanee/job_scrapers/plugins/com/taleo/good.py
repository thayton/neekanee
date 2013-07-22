from neekanee.jobscrapers.taleo.taleo import TaleoJobScraper

COMPANY = {
    'name': 'Good Technology',
    'hq': 'Sunnyvale, CA',

    'home_page_url': 'http://www1.good.com',
    'jobs_page_url': 'http://tbe.taleo.net/CH11/ats/careers/jobSearch.jsp?org=GOOD&cws=1',

    'empcnt': [501,1000]
}

class GoodJobScraper(TaleoJobScraper):
    def __init__(self):
        super(GoodJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[-1].text)

def get_scraper():
    return GoodJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
