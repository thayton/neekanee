from neekanee.jobscrapers.taleo.taleo import TaleoJobScraper

COMPANY = {
    'name': 'CEDA International Corporation',
    'hq': 'Calgary, Canada',

    'ats': 'Taleo',

    'home_page_url': 'http://www.cedagroup.com',
    'jobs_page_url': 'http://bc.tbe.taleo.net/BC12/ats/careers/jobSearch.jsp?org=CEDAINTE2&cws=1',

    'empcnt': [1001,5000]
}

class CedaJobScraper(TaleoJobScraper):
    def __init__(self):
        super(CedaJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        l = td[2].text + ', Canada'
        return self.parse_location(l)

def get_scraper():
    return CedaJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
