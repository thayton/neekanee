from neekanee.jobscrapers.taleo.taleo import TaleoJobScraper

COMPANY = {
    'name': 'Interweave',
    'hq': 'Loveland, CO',

    'home_page_url': 'http://www.interweave.com',
    'jobs_page_url': 'https://tbe.taleo.net/CH04/ats/careers/jobSearch.jsp?org=INTERWEAVE&cws=1',

    'empcnt': [51,200]
}

class InterweaveJobScraper(TaleoJobScraper):
    def __init__(self):
        super(InterweaveJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[1].text)

def get_scraper():
    return InterweaveJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
