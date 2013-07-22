from neekanee.jobscrapers.taleo.taleo import TaleoJobScraper

COMPANY = {
    'name': 'Various',
    'hq': 'Boca Raton, FL',

    'home_page_url': 'http://www.various.com',
    'jobs_page_url': 'http://ch.tbe.taleo.net/CH10/ats/careers/jobSearch.jsp?org=VARIOUS&cws=1',

    'empcnt': [11,50]
}

class VariousJobScraper(TaleoJobScraper):
    def __init__(self):
        super(VariousJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[-1].text)

def get_scraper():
    return VariousJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()

