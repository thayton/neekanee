from neekanee.jobscrapers.taleo.taleo import TaleoJobScraper

COMPANY = {
    'name': 'Canadian Natural',
    'hq': 'Calgary, Canada',

    'home_page_url': 'http://www.cnrl.com',
    'jobs_page_url': 'http://ch.tbe.taleo.net/CH09/ats/careers/jobSearch.jsp?org=CNRL&cws=1',

    'empcnt': [5001,10000]
}

class CrnlJobScraper(TaleoJobScraper):
    def __init__(self):
        super(CrnlJobScraper, self).__init__(COMPANY)

    def get_location_from_td(self, td):
        return self.parse_location(td[-1].text)

def get_scraper():
    return CrnlJobScraper()

if __name__ == '__main__':
    job_scraper = get_scraper()
    job_scraper.scrape_jobs()
