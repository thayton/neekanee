from neekanee.jobscrapers.taleo.taleo import TaleoJobScraper

COMPANY = {
    'name': 'Bonnier Corporation',
    'hq': 'Winter Park, FL',

    'ats': 'Taleo',

    'home_page_url': 'http://www.bonniercorp.com',
    'jobs_page_url': 'http://tbe.taleo.net/CH04/ats/careers/jobSearch.jsp?org=worldpub&cws=1',

    'empcnt': [501,1000]
}

class BonnierCorpJobScraper(TaleoJobScraper):
    def __init__(self):
        super(BonnierCorpJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[1].text)

def get_scraper():
    return BonnierCorpJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
