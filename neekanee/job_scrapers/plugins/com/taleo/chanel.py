from neekanee.jobscrapers.taleo.taleo import TaleoJobScraper

COMPANY = {
    'name': 'Chanel',
    'hq': 'Paris, France',

    'ats': 'Taleo',

    'home_page_url': 'http://www.chanel.com',
    'jobs_page_url': 'http://tbe.taleo.net/CH01/ats/careers/jobSearch.jsp?org=CHANEL&cws=1',

    'empcnt': [10001]
}

class ChanelJobScraper(TaleoJobScraper):
    def __init__(self):
        super(ChanelJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[-1].text)

def get_scraper():
    return ChanelJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
