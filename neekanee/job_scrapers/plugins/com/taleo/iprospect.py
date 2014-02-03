from neekanee.jobscrapers.taleo.taleo import TaleoJobScraper

COMPANY = {
    'name': 'iProspect',
    'hq': 'Boston, MA',

    'ats': 'Taleo',

    'home_page_url': 'http://www.iprospect.com',
    'jobs_page_url': 'http://ch.tbe.taleo.net/CH03/ats/careers/jobSearch.jsp?org=CARAT&cws=58',

    'empcnt': [51,200]
}

class iProspectJobScraper(TaleoJobScraper):
    def __init__(self):
        super(iProspectJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[-1].text)

def get_scraper():
    return iProspectJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
