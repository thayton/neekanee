from neekanee.jobscrapers.taleo.taleo import TaleoJobScraper

COMPANY = {
    'name': 'Enerplus',
    'hq': 'Calgary, Canada',

    'home_page_url': 'http://www.enerplus.com',
    'jobs_page_url': 'http://tbe.taleo.net/CH06/ats/careers/jobSearch.jsp?org=ENERPLUS&cws=1',

    'empcnt': [501,1000]
}

class EnerplusJobScraper(TaleoJobScraper):
    def __init__(self):
        super(EnerplusJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[1].text)

def get_scraper():
    return EnerplusJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
