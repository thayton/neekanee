from neekanee.jobscrapers.taleo.taleo import TaleoJobScraper

COMPANY = {
    'name': 'Symbio',
    'hq': 'San Jose, CA',

    'ats': 'Taleo',

    'home_page_url': 'http://www.symbio.com',
    'jobs_page_url': 'http://tbe.taleo.net/CH11/ats/careers/jobSearch.jsp?org=SYMBIO&cws=1',

    'empcnt': [1001,5000]
}

class SymbioJobScraper(TaleoJobScraper):
    def __init__(self):
        super(SymbioJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[-1].text)

def get_scraper():
    return SymbioJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
