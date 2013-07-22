from neekanee.jobscrapers.taleo.taleo import TaleoJobScraper

COMPANY = {
    'name': 'Lancope',
    'hq': 'Alpharetta, GA',

    'home_page_url': 'http://lancope.com',
    'jobs_page_url': 'http://ch.tbe.taleo.net/CH03/ats/careers/jobSearch.jsp?org=LANCOPE&cws=1',

    'empcnt': [51,200]
}

class LancopeJobScraper(TaleoJobScraper):
    def __init__(self):
        super(LancopeJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        l = td[-1].text
        l = l.rsplit('-', 1)[0]
        return self.parse_location(l)

def get_scraper():
    return LancopeJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
