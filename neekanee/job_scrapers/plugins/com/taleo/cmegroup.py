from neekanee.jobscrapers.taleo.taleo import TaleoJobScraper

COMPANY = {
    'name': 'CME Group',
    'hq': 'Chicago, IL',

    'ats': 'Taleo',

    'home_page_url': 'http://www.cmegroup.com',
    'jobs_page_url': 'http://tbe.taleo.net/CH11/ats/careers/jobSearch.jsp?org=CMEGROUP&cws=1',

    'empcnt': [1001,5000]
}

class CmeGroupJobScraper(TaleoJobScraper):
    def __init__(self):
        super(CmeGroupJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        l = td[1].text
        l = l.split(',')[0]
        return self.parse_location(l)

def get_scraper():
    return CmeGroupJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
